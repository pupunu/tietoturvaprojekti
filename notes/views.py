from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import requests
from django.http import HttpResponse


from django.http import HttpResponse

from .models import Note

#allowed_urls = ["https://fi.wikipedia.org", "https://en.wikipedia.org"] #!!! Part of correction for flaw 5. Add any other allowed sources here


@login_required
def index(request):
    notes_list = list(Note.objects.filter(owner = request.user))
    for index, note in enumerate(notes_list):
        if note.text.startswith("http"): #Flaw 5 correction: replace this row with --> if any(note.text.startswith(allowed_url) for allowed_url in allowed_urls)
            notes_list[index] = Note(id = note.id, text = requests.get(note.text).text)
    context = {'notes_list':notes_list, "user":request.user}
    return render(request, "notes/index.html", context)

@login_required
def add(request):
    text = request.POST.get('note')

    if text != "":
        user = User.objects.filter(username = request.POST.get('user'))[0] #FLAW3 correction: remove
        note = Note.objects.create(text = text, owner = user) #FLAW3 correction: remove
        #Flaw 3: replace 2 rows above with 1 row below
        #note = Note.objects.create(text = text, owner = request.user)
    return redirect("/")

@login_required
def delete(request, note_id):
    note = Note.objects.filter(id = note_id)[0] #FLAW 7: replace with note = Note.objects.filter(id = note_id, owner = request.user)[0]
    note.delete()
    return redirect("/")

@login_required
def filter(request):
    filter_word = request.GET.get("filter_word")
    notes_list = Note.objects.raw("SELECT * FROM notes_note WHERE owner_id = " + str(request.user.id) + " AND text like '%" + filter_word + "%'")
    # Flaw 2: Replace row above with: notes_list = Note.objects.filter(owner = request.user, text__contains=filter_word)
    context = {'notes_list':notes_list, "user":request.user}
    return render(request, "notes/index.html", context)

def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    if User.objects.filter(username = username).exists():
        return HttpResponse("Username already taken!!!")

    # Flaw 6 correction: add lines below
    #elif len(password) < 5 or username in password: #could also add checking common passwords or speacial characters
    #    return HttpResponse("Your password should be at least 6 characters long!!!")

    else:
        user = User.objects.create_user(username, "", password)
        return redirect("/")    
