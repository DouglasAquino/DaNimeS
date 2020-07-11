from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password
from audioop import reverse
from random import randint

def inicial(request):
    perso=Personagem_Risada.objects.all()
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

lista=[]
def gera():
    listaP=Personagem_Risada.objects.all()
    x = randint(0,len(listaP)-1)
    perso=Personagem_Risada.objects.filter(pk=x)
    if perso.exists():
        personagem=Personagem_Risada.objects.get(pk=x)
        lista.append(personagem)
        return personagem
    else:
        gera()


def quiz_risadas(request):
    perso=gera()
    lista_botoes=[]
    tudo=Personagem_Risada.objects.all()
    cont=0
    for i in tudo:
        lista_botoes.append(i)
        cont+=1
        if cont == 4:
            break
    return render(request, 'app_anime/quiz_risadas.html', {'perso': perso, 'lista':lista_botoes})


def quiz_Op(request):
    openings = Op_Anime.objects.all()
    return render(request, 'app_anime/quiz_openings.html', {'OP': openings})