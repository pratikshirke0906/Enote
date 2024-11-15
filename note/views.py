from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, NoteForm
from .models import Note

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'notes': notes})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('dashboard')
    else:
        form = NoteForm()
    return render(request, 'add_note.html', {'form': form})

@login_required
def edit_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = NoteForm(instance=note)
    return render(request, 'edit_note.html', {'form': form})

@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    note.delete()
    return redirect('dashboard')

def user_logout(request):
    logout(request)
    return redirect('home')
