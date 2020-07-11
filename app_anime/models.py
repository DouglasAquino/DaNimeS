from django.db import models
from django.contrib.auth.models import User



class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, blank= True, null= True)
    nome= models.CharField(max_length= 10, blank= True, null= True)

    def __str__(self):
        return '{} - {}'.format(self.nome, self.user)


class Personagem_Risada(models.Model):
    nome= models.CharField(max_length= 15, blank= True, null= True)
    imagem= models.ImageField(upload_to = 'Imagem') 
    onomatopeia= models.CharField(max_length= 15, blank= True, null= True)
    risada = models.FileField(upload_to = 'Risada')

    def __str__(self):
        return self.nome


class Xp(models.Model):
    usuario= models.ForeignKey(Usuario, on_delete= models.CASCADE, blank= True, null= True)
    qt_pontos= models.IntegerField()

    def __str__(self):
        return '{} - {}'.format(self.usuario, self.qt_pontos)


class Op_Anime(models.Model):
    nome= models.CharField(max_length= 21, blank= True, null= True)
    opening = models.FileField(upload_to = 'Opening')

    def __str__(self):
        return self.nome

