from django.urls import path
from . import views

app_name = 'sis_cadastros'

urlpatterns = [
    path('fornecedor/', views.tb_fornecedor, name='tb_fornecedor'),
    path('fornecedor/novo/', views.nv_fornecedor, name='nv_fornecedor'),
    path('fornecedor/novo/resposta', views.cad_fornecedor, name='cad_fornecedor'),
]