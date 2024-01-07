from django.db import models


class Teacher(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')

    class Meta:
        app_label = 'stakler'
    

class Subject(models.Model):
    semester = models.CharField(max_length=100, default='')
    ects = models.IntegerField()
    name = models.CharField(max_length=100, default='')
    owner = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        app_label = 'stakler'

class Group(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date_time = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    limit = models.CharField(default='0')
    enrolled = models.CharField(default='0')
    queue = models.CharField(default='0')

    class Meta:
        app_label = 'stakler'
