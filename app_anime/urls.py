from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import inicial, cadastrar
from django.conf.urls import url
import audioop


urlpatterns = [
    path('',inicial,name="inicial"),
    path('cadastrar',cadastrar,name="cadastrar"),
    # Here we mount the app under /music. Feel free to use something else
    #url(r'^$', include(' '), name='home'),
    #url("risada", include("audiotracks.urls")),
    # Some URLs require a Django username
    #url("^(?P<username>[\w\._-]+)/music", include("audiotracks.urls")),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)