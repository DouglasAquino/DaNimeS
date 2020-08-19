from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import inicial, cadastrar, quiz_risadas, quiz_Op, wanted, acertou_op, errou_op, game_over,acertou_ri,errou_ri,sobre
from django.conf.urls import url
import audioop

urlpatterns = [
    path('',inicial,name="inicial"),
    path('game_over',game_over,name="game_over"),
    path('cadastrar',cadastrar,name="cadastrar"),
    path('sobre',sobre,name="sobre"),
    path('acertou/<int:pontos>',acertou_op,name="acertou_op"),
    path('errou/<int:pontos>',errou_op,name="errou_op"),

    path('acertou_ri/<int:pontos>',acertou_ri,name="acertou_ri"),
    path('errou_ri/<int:pontos>',errou_ri,name="errou_ri"),

    path('wanted',wanted,name="wanted"),
    path('quiz_risadas',quiz_risadas,name="quiz_risadas"),
    path('quiz_opening', quiz_Op, name="quiz_openings"),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
