import os
from typing import Iterator

from bs4 import BeautifulSoup as bs
from django.core.management.base import BaseCommand
from stakler.models import Group, Subject, Teacher


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def _extract_table(self, filename: str) -> tuple[list[str], list[str]]:
        """ Returns parsed data from html file containing overview of the subject page.
        So it is not meant for extracting list of enrolled and waiting students.
        """
        with open(filename, 'r', encoding="utf-8") as general:
            site = bs(general, 'html.parser')
            general.close()

        tables = site.find_all('table')
        first_table_id = 0
        table_headers = list(map(lambda y:y.contents[first_table_id],
                                tables[first_table_id].find_all('th')))
        table_data = tables[first_table_id].find_all('td')

        for i, j in enumerate(table_data):
            table_data[i] = list(filter(lambda x:x!='\n', j.contents))
        """
        table headers represent names of the field in the database
        what I actually need is
        """

        return (table_headers, table_data)

    # can be used build_from_table(extract_table(arg)[1])
    def _build_from_table(self, table_data: list[str]) -> list[str]:
        """ Returns cleaned up input list.
        Some entries contain multiple whitespaces and other artifacts, are in incorrect
        format, etc. so fixing all that issues is necessary.
        It seems to me that it should be in part replaced by parsing the json file
        but I still think a part of this should be useful.
        """
        clean_table_data = []
        full_names = {'(wyk.)': 'lecture', '(ćw.)': 'exercise', '(prac.)': 'lab',
                '(ćw-prac.)' : 'lab-exercise', '(rep.)' : 'rep', '(sem.)' : 'sem'}
        yes_or_no = {'Nie' : False, 'Tak' : True}
        # I have no idea what this loop was all about
        for i, j in enumerate(table_data):
            if i == 1:
                tmp = list(filter(lambda x:x !='', table_data[1][0]['href'].split('/')))
                clean_table_data.append(tmp[-1])
                continue
            if i == 2:
                tmp = list(map(lambda x:x.contents[0], j[1:]))
                clean_table_data.append(tmp)
                continue
            try:
                tmp = table_data[i][0].contents[0]
            except:
                tmp = table_data[i][0]
            clean_table_data.append(tmp.strip())

        clean_table_data[2] = {full_names[ys.split()[1]]:ys.split()[0]
                            for ys in clean_table_data[2]}

        for v in full_names.values():
            clean_table_data[2].setdefault(v, '')

        clean_table_data[2] = dict(sorted(clean_table_data[2].items()))
        clean_table_data[5] = yes_or_no[clean_table_data[5]]
        clean_table_data[6] = yes_or_no[clean_table_data[6]]

        return clean_table_data


    def _extract_individual(self, t):
        tmp = []
        # first table row only contains field names which are the same
        # every time
        for trs in t.find_all('tr')[1:]:
            current_group = []
            for cnt, tds in enumerate(trs.find_all('td')[:-1]):
                if cnt == 0:
                    href = tds.find('a')['href']
                    teacher_id = ''.join(list(filter(str.isdecimal, href)))
                    teacher_id = int(teacher_id)
                    current_group.append(teacher_id)
                elif cnt == 1:
                    evs = [ev.contents[0] for ev in tds.find_all('span')]
                    current_group.append(evs)
                else:
                    try:
                        val = ''.join(tds.contents[0].split()) + tds.contents[1].contents[0].strip()
                    except:
                        val = tds.contents[0].strip()
                    current_group.append(val)
            tmp.append(current_group)
        return tmp


    def _extract_group_data(self, path: str):
        with open(path, 'r', encoding="utf-8") as f:
            site = bs(f, 'html.parser')
        result = {}
        """
        table headers are as follows:
        teacher
        event time
        limit
        zapisani
        kolejka
        there is also some empty th tag but I do not need it
        regardless of whatever would be supposed to be there
        it is probably the url but I do not care about it
        """
        for t in site.find_all('div', {'class' : 'table-responsive'}):
            tmp = self._extract_individual(t)
            curr_key = t.find('h3').contents[0].strip()
            result[curr_key] = tmp
        return result


    def _gen_files(self, path: str) -> Iterator[str]:
        """
        I now realised (2023-10-09) that actually finding files like that is dreary
        as some of needed information is stored (or should be) by my design in
        subjects.json for each and every semester
        """
        for root, _, files in os.walk(path):
            for file in files:
                file_name: str = file.split('.')[0]
                file_extension: str = file.split('.')[1]
                if not file_name.isdecimal() and file_extension == 'html':
                    yield os.path.join(root, file)


    def _full_info(self, path: str):
        res1 = self._build_from_table(self._extract_table(path)[1])
        # res1 represents the subject to add
        res2 = self._extract_group_data(path)
        # res2 contains groups this subject groups
        with open(path, 'r', encoding="utf-8") as fp:
            s = bs(fp, 'html.parser')
            name = s.find('h1').contents[0].strip()
            semester = s.find('h1').contents[1].contents[0].strip()
        # print(res1[1], res1[4], name, semester)
        try:
            Teacher.objects.get(pk=res1[1])
        except Teacher.DoesNotExist:
            res1[1] = 0

        teach = Teacher.objects.get(pk=res1[1])

        obj, _ = Subject.objects.get_or_create(
            semester=semester,
            ects=res1[4],
            name=name,
            owner=teach,
        )
        for keys, vals in res2.items():
            for val in vals:
                times = ','.join(val[1])

                try:
                    Teacher.objects.get(pk=val[0])
                except Teacher.DoesNotExist:
                    val[0] = 0


                teach = Teacher.objects.get(pk=val[0])

                Group.objects.get_or_create(
                    subject=obj,
                    teacher=teach,
                    date_time=times,
                    name=keys,
                    limit=val[2],
                    enrolled=val[3],
                    queue=val[4],
                )


    def handle(self, *args, **options):
        path='/app/stakler/semesters/'
        for p in self._gen_files(path):
            self._full_info(p)
        # path = '/app/stakler/semesters'
