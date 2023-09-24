from django.urls import path

from . import views

urlpatterns = [
    # ex: /notes/
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("delete/<int:note_id>", views.delete, name="delete"),
]