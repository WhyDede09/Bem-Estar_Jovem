from django.contrib.auth import views as auth
from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("guia/", views.guia, name="guia"),
    path("colega/", views.colega, name="colega"),
    path("relatar/", views.denunciar, name="denunciar"),
    path("relatar/enviado/", views.enviada, name="enviada"),
    path("acompanhar/", views.acompanhar, name="acompanhar"),
    path("coordenacao/entrar/", auth.LoginView.as_view(template_name="apoio/login.html"), name="login"),
    path("coordenacao/sair/", auth.LogoutView.as_view(), name="sair"),
    path("coordenacao/", views.painel, name="painel"),
    path("coordenacao/<int:pk>/", views.detalhe, name="detalhe"),
    path("coordenacao/<int:pk>/prova/", views.prova, name="prova"),
]
