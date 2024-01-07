from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Subject, Teacher, Group

def index(request):
    template = loader.get_template("stakler/index.html")
    # name context has to be defined
    # I guess that it is used for tempate parameters but since I do not
    # have any in here I just had to create an empty dict name context
    context = {}
    return HttpResponse(template.render(context, request))


def subject(request):
    current_subject_list = Subject.objects.distinct('name')
    template = loader.get_template("stakler/subject.html")
    # name context has to be defined
    # I guess that it is used for tempate parameters but since I do not
    # have any in here I just had to create an empty dict name context
    context = {
        'current_subject_list' : current_subject_list,
    }
    return HttpResponse(template.render(context, request))


def teacher_list(request):
    teachers = Teacher.objects.all()
    template = loader.get_template('stakler/teacher.html')
    context = {
        'teachers' : teachers,
    }
    return HttpResponse(template.render(context, request))


def teacher_detail(request, teacher_id):
    teacher = Teacher.objects.get(pk=teacher_id)
    teacher_groups_list = Group.objects.filter(teacher=teacher)
    template = loader.get_template('stakler/teacher_detail.html')
    context = {
        'teacher_groups_list' : teacher_groups_list,
        'teacher' : teacher,
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse('Currently looking at %s' % teacher_id)


def subject_detail(request, subject_id):
    # to replace detail
    sub = Subject.objects.get(pk=subject_id)
    template = loader.get_template('stakler/subject_detail.html')
    groups = Group.objects.filter(subject__name__exact=sub.name)
    context = {
        'groups' : groups,
        'sub' : sub,
    }
    return HttpResponse(template.render(context, request))
