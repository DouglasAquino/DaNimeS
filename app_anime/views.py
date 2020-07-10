from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password
from audioop import reverse

def inicial(request):
    perso=Personagem.objects.all()
    return render(request, 'app_anime/inicial.html', {'perso': perso})

def cadastrar(request):
    if request.method=="GET":
        form=CadastrarForm()
        return render(request, 'app_anime/Cadastrar.html', {'form':form})

    elif request.method=="POST":
        user=User()
        user.username=request.POST['nome']
        user.password=make_password(request.POST['senha'])
        user.save()

        usuario=Usuario()
        usuario.nome=request.POST['nome']
        usuario.user=user
        usuario.save()
        return redirect(reverse, 'inicial')