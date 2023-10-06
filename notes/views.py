from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.


from django.http import HttpResponse

from .models import Note

@login_required
def index(request):
    notes_list = Note.objects.filter(owner = request.user)
    context = {'notes_list':notes_list, "user":request.user}
    return render(request, "notes/index.html", context)

@login_required
def add(request):
    text = request.POST.get('note')

    if text != "":
        user = User.objects.filter(username = request.POST.get('user'))[0] #flaw correction: remove
        note = Note.objects.create(text = text, owner = user) #flaw correction: remove
        #Flaw 3: replace 2 rows above with 1 row below
        #note = Note.objects.create(text = text, owner = request.user)
    return redirect("/")

@login_required
def delete(request, note_id):
    note = Note.objects.filter(id = note_id)[0]
    note.delete()
    return redirect("/")

@login_required
def filter(request):
    filter_word = request.GET.get("filter_word")
    notes_list = Note.objects.raw("SELECT * FROM notes_note WHERE owner_id = " + str(request.user.id) + " AND text like '%" + filter_word + "%'")
    # Flaw 2: Replace row above with: notes_list = Note.objects.filter(owner = request.user, text__icontains=filter_word)
    context = {'notes_list':notes_list, "user":request.user}
    return render(request, "notes/index.html", context)

def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = User.objects.create_user(username, "", password)
    return redirect("/")