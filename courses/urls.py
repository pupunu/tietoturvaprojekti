from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("course/<int:course_id>", views.course, name="course"),
    path("teacher", views.teacher, name="teacher"),
    path("teacher/<int:course_id>", views.teacher_edit, name="teacher_edit")
]