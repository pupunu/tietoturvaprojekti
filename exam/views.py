from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

#from .models import 


def index(request  ):
    return render(request, "exam/index.html")

def quiz(request, question_id):
    response = "The question is " + str(question_id)
    return HttpResponse(response)

def points(request, question_id):
    response = "Ei mitään pisteitä täällä"