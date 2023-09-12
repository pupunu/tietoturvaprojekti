from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request  ):
    return HttpResponse("Täällä pitää harjoitella tehtäviä")

def quiz(request, question_id):
    response = "The question is " + str(question_id)
    return HttpResponse(response)