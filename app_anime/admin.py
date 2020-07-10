from django.contrib import admin
from .models import Op_Anime, Personagem_Risada, Usuario, Xp

@admin.register(Op_Anime)
@admin.register(Personagem_Risada)
@admin.register(Usuario)
@admin.register(Xp)


class Anime(admin.ModelAdmin):
    pass
