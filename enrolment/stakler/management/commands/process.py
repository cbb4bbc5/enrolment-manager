from django.core.management.base import BaseCommand, CommandError

import sys, os, json
from typing import Iterator

from stakler.models import Teacher

# I tried to make it into a standalone script but every
# way to do so that I found failed in way or another, mostly related
# to settings, modules not existing, being duplicated, meta classes
# I just gave up and made it into a command for manage.py this was
# actually what I needed in this case so it acceptable
# https://forum.djangoproject.com/t/using-django-settings-module-in-a-script-in-subfolder/3032/3
class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """ I had to create additional function which is similar to
            extract_course_data but different in some key aspects so
            I decided to just create a new one instead of modifying
            the existing one
        """
        path = '/app/stakler/teachers.json'
        # TODO: make it not hardcoded
        # https://stackoverflow.com/questions/57472578/python-how-to-pass-command-line-arg-as-string-instead-of-tuple
        with open(path, 'r') as teachers:
            #contents = subjects.read()
            json_data = json.load(teachers)

        teacher_info = list(json_data.values())

        for teacher in teacher_info:
            first_name = teacher['first_name']
            last_name = teacher['last_name']
            id = teacher['id']
            Teacher.objects.get_or_create(id=id, first_name=first_name, last_name=last_name)


