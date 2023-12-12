from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registo_encomenda/', views.registo_encomenda, name='registo_encomenda'),
    path('producao_equipamentos/', views.producao_equipamentos, name='producao_equipamentos'),
    path('registar_equipamento/', views.registar_equipamento, name='registar_equipamento'),
    path('vendas_equipamentos/', views.vendas_equipamentos, name='vendas_equipamentos'),
    path('gestao_clientes/', views.gestao_clientes, name='gestao_clientes'),
]