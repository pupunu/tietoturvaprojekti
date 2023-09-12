from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quiz/<int:question_id>/", views.quiz, name = "quiz"),
    path("quiz/<int:question_id>/points/", views.points, name='points'),
]