from django.shortcuts import render
from courses.models import *
from django.contrib.auth.models import User
from database import get_course
import sqlite3

# Create your views here.

def index(request):
    return render(request, "courses/index.html")

def course(request, course_id):
    db = sqlite3.connect("database.db")
    db.isolation_level = None
    c = get_course(db, course_id)
    context = {"course":c,}
    return render(request, "courses/course-student.html", context)

def teacher(request):
    #courses = [e for e in Course.objects.all() if course.teacher == None]
    return render(request, "courses/teacher.html")

def teacher_edit(request, course_id):
    pass
