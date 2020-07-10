from django import forms
from .models import *
from django.contrib.auth.forms import User,UserCreationForm

class CadastrarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields=['nome']
    senha = forms.CharField(widget=forms.PasswordInput)
    