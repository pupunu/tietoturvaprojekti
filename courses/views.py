from django.shortcuts import render
from courses.models import *

# Create your views here.

def index(request):
    return render(request, "courses/index.html")

def course(request, course_id):
    c = Course(name="test")
    q1 = Question(text="Mikä on kello?")
    q2 = Question(text="Mikä on sello?")
    q1a1 = Answer(text="laite", right=True)
    q1a2 = Answer(text="Sello", right=False)
    q2a1 = Answer(text="Soitin", right=True)
    q2a2 = Answer(text="Jätekasa", right=False)
    q1.answers.append(q1a1)
    q1.answers.append(q1a2)
    q2.answers.append(q2a1)
    q2.answers.append(q2a2)
    c.questions.append(q1)
    c.questions.append(q2)

    context = {"course":c,
    }
    return render(request, "courses/course-student.html", context)