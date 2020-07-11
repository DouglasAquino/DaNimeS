from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import inicial, cadastrar, quiz_risadas, quiz_Op, wanted
from django.conf.urls import url
import audioop

urlpatterns = [
    path('',inicial,name="inicial"),
    path('cadastrar',cadastrar,name="cadastrar"),
    path('wanted',wanted,name="wanted"),
    path('quiz_risadas',quiz_risadas,name="quiz_risadas"),
    path('quiz_opening', quiz_Op, name="quiz_openings"),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)