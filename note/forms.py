from django import forms
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description']
