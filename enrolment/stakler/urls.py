from django.urls import path

from . import views

app_name='stakler'

urlpatterns = [
    path('', views.index, name='index'),
    path('subjects', views.subject, name='subject'),
    path("subjects/<int:subject_id>/", views.subject_detail, name="detail"),
    path('teachers/', views.teacher_list, name='teachers'),
    # this name=... is what you provide in the template, not views....
    # I wasted so much time because of this
    path("teachers/<int:teacher_id>/", views.teacher_detail, name="td"),
]
