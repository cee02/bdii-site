from django.urls import path
from . import views
from .views import gestao_clientes

urlpatterns = [
<<<<<<< HEAD
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('', views.logout, name='c_logout'),
=======
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
>>>>>>> parent of fbd4a88 (Teste1- logout)
    path('error_page/<str:error_message>/', views.error_page, name='error_page'),
    path('dashboard/', views.dashboard, name='bdii_dashboard'),
    path('registo_encomenda/', views.registo_encomenda, name='bdii_registo_encomenda'),
    path('producao_equipamentos/', views.producao_equipamentos, name='bdii_producao_equipamentos'),
    path('registar_equipamento/', views.registar_equipamento, name='bdii_registar_equipamento'),
    path('vendas_equipamentos/', views.vendas_equipamentos, name='bdii_vendas_equipamentos'),
    path('gestao_clientes/', views.gestao_clientes, name='bdii_gestao_clientes'),
    path('delete-cliente/<int:cliente_id>/', views.delete_cliente, name='delete_cliente'),

]

