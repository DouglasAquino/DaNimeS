from django import forms
from .models import Usuario
from django.contrib.auth.forms import User

class CadastrarForm(forms.Form):
    username = forms.CharField(max_length=50)
    senha = forms.CharField(widget=forms.PasswordInput)

class cadastrarF(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'imagem']


