from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.


from django.http import HttpResponse

from .models import Note

@login_required
def index(request):
    notes_list = Note.objects.filter(owner = request.user)
    context = {'notes_list':notes_list}
    return render(request, "notes/index.html", context)

@login_required
def add(request):
    text = request.POST.get('note')
    if text != "":
        note = Note.objects.create(text = text, owner = request.user)
    return redirect("/")

@login_required
def delete(request, note_id):
    Note.objects.remove(id = note_id)
    return redirect("/")
