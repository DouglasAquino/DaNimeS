from django.contrib import admin
from .models import Anime, Personagem, Usuario, Xp

@admin.register(Anime)
@admin.register(Personagem)
@admin.register(Usuario)
@admin.register(Xp)


class Anime(admin.ModelAdmin):
    pass
