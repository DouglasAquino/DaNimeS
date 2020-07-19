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

def gerabtns_ri(indice):
    botoes=[]
    if Personagem_Risada.objects.filter(pk=indice):
        certo=Personagem_Risada.objects.get(pk=indice)
        botoes.append(certo.nome)
        lista=Personagem_Risada.objects.all()
        pks=[]
        for i in lista:
            pks.append(i.pk)

        
        while len(botoes)!= 4:
            for k in pks:
                if Personagem_Risada.objects.filter(pk=k):
                    errado=Personagem_Risada.objects.get(pk=k)
                    if errado.nome not in botoes:
                        botoes.append(errado.nome)
                        break
                    
        
        botoes.sort()
    
        return botoes

global risada
def sorteia_Ri(cont):
    global risada
    risada=[]
    if cont >=4:
        risada=[]
    lista=list(Personagem_Risada.objects.all())
    pk=randint(1,len(lista))
    if pk not in risada:
        if Personagem_Risada.objects.filter(pk=pk):
            risada.append(pk)
            return pk
        else:
            cont+=1
            sorteia_Ri(cont)
    else:
        cont+=1
        sorteia_Ri(cont)

def quiz_risadas(request):
    usuario=Usuario.objects.get(user=request.user)
    indice=sorteia_Ri(0)
    perso=Personagem_Risada.objects.get(pk=indice)
    botoes=gerabtns_ri(indice)
    return render(request, 'app_anime/quiz_risadas.html', {'perso': perso, 'usuario':usuario, 'botoes':botoes})

global openings
openings=[]
def sorteia_OP():
    global openings
    lista=list(Op_Anime.objects.all())
    if len(openings) == len(lista):
        openings=[]
    pk=randint(1,len(lista))
    if pk not in openings:
        if Op_Anime.objects.filter(pk=pk):
            openings.append(pk)
            return pk
        else:
            sorteia_OP(cont)
    else:
        sorteia_OP(cont)

def gerabtns_OP(indice):
    botoes=[]
    if Op_Anime.objects.filter(pk=indice):
        certo=Op_Anime.objects.get(pk=indice)
        botoes.append(certo.nome)
        lista=Op_Anime.objects.all()
        pks=[]
        for i in lista:
            pks.append(i.pk)

        
        while len(botoes)!= 4:
            k=randint(0,len(pks))
            if Op_Anime.objects.filter(pk=k):
                errado=Op_Anime.objects.get(pk=k)
                if errado.nome not in botoes:
                    botoes.append(errado.nome)
                    
        
        botoes.sort()
    
        return botoes

def quiz_Op(request):
    indice=sorteia_OP()
    botoes=gerabtns_OP(indice)
    ope = Op_Anime.objects.get(pk = indice)
    xp=Xp.objects.get(usuario__nome=request.user)
    return render(request, 'app_anime/quiz_openings.html', {'OP': ope,'botoes':botoes,'xp':xp})

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

def acertou(request):
    if request.user.is_authenticated:
        usuario=Usuario.objects.filter(user=request.user)
        if usuario.exists():
            usuario=Usuario.objects.get(nome=request.user)
            xp=Xp.objects.get(usuario=usuario)
            xp.qt_pontos+=10
            xp.save()

            return quiz_Op(request)
