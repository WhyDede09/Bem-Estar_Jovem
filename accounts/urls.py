from django.urls import path

from . import views

urlpatterns = [
    path("coordenacao/entrar/", views.entrar, name="login"),
    path("coordenacao/sair/", views.sair, name="sair"),
]
