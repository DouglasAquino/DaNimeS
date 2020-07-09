from django.shortcuts import render
from .models import *

def inicial(request):
    perso=Personagem.objects.all()
    return render(request, 'app_anime/inicial.html', {'perso': perso})