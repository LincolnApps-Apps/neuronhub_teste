from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'core_website'

urlpatterns = [
    path('', views.apresentacao, name='apresentacao'),
    path('cadastrar-se/', views.cadastro_novo_negocio, name='cadastro_novo_negocio'),
    path('accounts/login/', views.login, name='login'),
    path('login/sucesso/', views.login_view, name='login_sucesso'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('sucesso/', views.sucesso, name='sucesso'),
]
