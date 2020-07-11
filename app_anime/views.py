from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password
from audioop import reverse
from random import randint
from django.http import HttpResponse
from django.conf.urls import url
from django.core.files.storage import FileSystemStorage

def inicial(request):
    perso=Personagem_Risada.objects.all()
    return render(request, 'app_anime/inicial.html', {'perso': perso})

def cadastrar(request):
    if request.method=="GET":
        form=CadastrarForm()
        return render(request, 'app_anime/Cadastrar.html', {'form':form})

    elif request.method=="POST" and request.FILES['imagem']:
        myfile = request.FILES['imagem']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        user=User()
        user.username=request.POST['nome']
        user.password=make_password(request.POST['senha'])
        user.save()

        #img=handle_uploaded_file(request.FILES['imagem'])

        usuario=Usuario()
        usuario.nome=request.POST['nome']
        usuario.user=user
        usuario.imagem=uploaded_file_url
        usuario.save()
        return redirect('inicial')

lista=[]
def gera():
    listaP=Personagem_Risada.objects.all()
    x = randint(0,len(listaP)-1)
    perso=Personagem.objects.filter(pk=x)
    if perso.exists():
        personagem=Personagem.objects.get(pk=x)
        lista.append(personagem)
        return personagem
    else:
        gera()

def quiz_risadas(request):
    perso=gera()
    lista_botoes=[]
    tudo=Personagem.objects.all()
    cont=0
    for i in tudo:
        lista_botoes.append(i)
        cont+=1
        if cont == 4:
            break
    return render(request, 'app_anime/quiz_risadas.html', {'perso': perso, 'lista':lista_botoes})

ordenada=[]
def ordenar(lista):
    cont=0
    maior=0
    pos=None
    for i in lista:
        if i.qt_pontos > maior:
            maior=i.qt_pontos
            pos=cont
        cont+=1
    ordenada.append(lista[pos])
    lista.pop(pos)
    
    while len(lista)>0:
        ordenar(lista)

def wanted(request):
    if request.user.is_authenticated:
        usuario=Usuario.objects.filter(user=request.user)
        if usuario.exists():
            xp=Xp.objects.get(usuario__user=request.user)
            return render(request, 'app_anime/wanted.html', {'xp':xp})
        else:
            return HttpResponse('ERROR!!')
    else:
        return render(request, 'app_anime/erro_autenticacao.html', {})

