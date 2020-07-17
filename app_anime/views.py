from django.shortcuts import redirect, render, reverse
from .models import *
from .forms import CadastrarForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from random import randint
from django.db.models import Max

def inicial(request):
    perso=Personagem_Risada.objects.all()
    return render(request, 'app_anime/inicial.html', {'perso': perso})

def cadastrar(request):
    if request.method == 'GET':
        form = CadastrarForm()
        return render(request, 'app_anime/cadastrar.html', {'form': form})

    elif request.method == 'POST':
        try:
            usuario = User()
            usuario.username = request.POST['username']
            usuario.password = make_password(request.POST['senha'])
            usuario.save()
            
            jogador = Usuario()
            jogador.nome = request.POST['username']
            jogador.user = usuario
            jogador.save()

            xp= Xp()
            xp.usuario = jogador
            xp.qt_pontos = 0
            xp.save()

        except Exception:
            return render(request, 'app_anime/User_existente.html')

        return redirect(reverse('login'))

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
    openings = Op_Anime.objects.get(pk = 4)
    sla= maiores()
    return render(request, 'app_anime/quiz_openings.html', {'OP': openings, 'Ma': sla})

def Maiores():
    todos= list(Xp.objects.all())
    pontos= []
    for i in todos:
        pontos.append(i.qt_pontos)
    crescente=sorted(pontos)
    top=[]
    decre=[]
    for k in crescente:
        decre.insert(0,k)
    for z in range(10):
        if z >= len(decre):
            break
        top.append(decre[z])
    rank=[]
    for i in top:
        for x in todos:
            if i == x.qt_pontos and x not in rank:
                rank.append(x)    

    return rank

def wanted(request):
    if request.user.is_authenticated:
        usuario=Usuario.objects.filter(user=request.user)
        if usuario.exists():
            usuario=Usuario.objects.get(nome=request.user)
            if Xp.objects.filter(usuario=usuario):
                xp=Xp.objects.get(usuario=usuario)
            maiores=Maiores()
            return render(request, 'app_anime/wanted.html', {'xp':xp,'usuario':usuario,'lista':maiores})
        else:
            return HttpResponse('ERROR!!')