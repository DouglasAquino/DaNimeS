from django.db import models
from django.contrib.auth.models import User



class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, blank= True, null= True)
    nome= models.CharField(max_length= 10, blank= True, null= True)

    def __str__(self):
        return '{} - {}'.format(self.nome, self.user)


class Personagem(models.Model):
    nome= models.CharField(max_length= 15, blank= True, null= True)
    imagem= models.ImageField(upload_to = 'Pimagem') 
    onomatopeia= models.CharField(max_length= 15, blank= True, null= True)
    risada = models.FileField(upload_to = 'risada')

    def __str__(self):
        return self.nome


class Xp(models.Model):
    usuario= models.ForeignKey(Usuario, on_delete= models.CASCADE, blank= True, null= True)
    qt_pontos= models.IntegerField()

    def __str__(self):
        return '{} - {}'.format(self.usuario, self.qt_pontos)


class Anime(models.Model):
    nome= models.CharField(max_length= 20, blank= True, null= True)
    opening = models.FileField(upload_to = 'imagens')

    def __str__(self):
        return self.nome

