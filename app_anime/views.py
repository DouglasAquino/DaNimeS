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
risada=[]
def sorteia_Ri():
    global risada
    lista=list(Personagem_Risada.objects.all())
    if len(risada) == len(lista):
        risada=[]
        print('entrou igual')
    pk=randint(1,len(lista))
    if pk not in risada:
        if Personagem_Risada.objects.filter(pk=pk):
            risada.append(pk)
            print('lista: ',risada,'retorno',pk)
            return pk
        else:
            sorteia_Ri()
    else:
        sorteia_Ri()

global lista_errou_ri
lista_errou_ri=[]
def quiz_risadas(request):
    global lista_errou_ri
    lista_errou_ri=[]
    indice=None
    while indice == None:
        indice=sorteia_Ri()
    print(indice)
    perso=Personagem_Risada.objects.get(pk=indice)
    botoes=Personagem_Risada.objects.all()
    xp=Xp.objects.get(usuario__nome=request.user)
    pontos=10
    lista_errou_ri=[botoes,perso]
    
    return render(request, 'app_anime/quiz_risadas.html', {'perso':perso,'xp':xp,'botoes':botoes,'pontos':pontos})

global openings
openings=[]
def sorteia_OP():
    global openings
    lista=list(Op_Anime.objects.all())
    if len(openings) == len(lista):
        openings=[]
        print('entrou tudo')
    pk=randint(1,len(lista))
    if pk not in openings:
        if Op_Anime.objects.filter(pk=pk):
            openings.append(pk)
            print('lista',openings,'retorno',pk)
            return pk
        else:
            sorteia_OP()
    else:
        sorteia_OP()

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


global lista_errou
lista_errou=[]
def quiz_Op(request):
    global lista_errou
    lista_errou=[]
    indice=None
    while indice == None:
        indice=sorteia_OP()
    print(indice)
    botoes=gerabtns_OP(indice)
    ope = Op_Anime.objects.get(pk = indice)
    xp=Xp.objects.get(usuario__nome=request.user)
    pontos=10
    lista_errou=[botoes,ope]
    
    return render(request, 'app_anime/quiz_openings.html', {'OP': ope,'botoes':botoes,'xp':xp, 'pontos':pontos})

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

def acertou(request,pontos):
    if request.user.is_authenticated:
        usuario=Usuario.objects.filter(user=request.user)
        if usuario.exists():
            usuario=Usuario.objects.get(nome=request.user)
            xp=Xp.objects.get(usuario=usuario)
            xp.qt_pontos+=pontos
            xp.save()

            return quiz_Op(request)

def errou(request,pontos):
    global lista_errou
    if request.user.is_authenticated:
        usuario=Usuario.objects.filter(user=request.user)
        if usuario.exists():
            if pontos > 0:
                if pontos == 10:
                    pontos-=2
                elif pontos == 8:
                    pontos-=4
                elif pontos == 4:
                    pontos-=3
                else:
                    pontos=0
                    return errou(request,pontos)
                    
                usuario=Usuario.objects.get(nome=request.user)
                botoes=lista_errou[0]
                ope=lista_errou[1]
                xp=Xp.objects.get(usuario__nome=request.user)
                return render(request, 'app_anime/quiz_openings.html', {'OP': ope,'botoes':botoes,'xp':xp, 'pontos':pontos})
            else:
                return redirect('game_over')

def game_over(request):
    return render(request, 'app_anime/game_over.html',{})

def acertou_ri(request,pontos):
    if request.user.is_authenticated:
        usuario=Usuario.objects.filter(user=request.user)
        if usuario.exists():
            usuario=Usuario.objects.get(nome=request.user)
            xp=Xp.objects.get(usuario=usuario)
            xp.qt_pontos+=pontos
            xp.save()
            todas=list(Personagem_Risada.objects.all())
            global risada
            if len(risada) == len(todas):
                risada=[]
                return render(request, 'app_anime/game_over.html', {'text':'PARABENS VOCÊ ACERTOU TUDO!!'})
            return quiz_risadas(request)

def errou_ri(request,pontos):
    global lista_errou_ri
    if request.user.is_authenticated:
        usuario=Usuario.objects.filter(user=request.user)
        if usuario.exists():
            if pontos > 0:
                if pontos == 10:
                    pontos-=2
                elif pontos == 8:
                    pontos-=4
                elif pontos == 4:
                    pontos-=3
                else:
                    pontos=0
                    return render(request, 'app_anime/game_over.html', {'text':'VOCÊ ERROU O MAXIMO POSSÍVEL!!'})
                    
                usuario=Usuario.objects.get(nome=request.user)
                botoes=lista_errou_ri[0]
                ope=lista_errou_ri[1]
                xp=Xp.objects.get(usuario__nome=request.user)
                return render(request, 'app_anime/quiz_risadas.html', {'perso': ope,'botoes':botoes,'xp':xp, 'pontos':pontos})
            else:
                return redirect('game_over')            
