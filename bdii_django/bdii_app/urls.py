from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='user_login'),
    path('', views.logout, name='c_logout'),
    path('error_page/<str:error_message>/', views.error_page, name='error_page'),
    path('dashboard/', views.dashboard, name='bdii_dashboard'),
    path('registo_encomenda/', views.registo_encomenda, name='bdii_registo_encomenda'),
    path('producao_equipamentos/', views.producao_equipamentos, name='bdii_producao_equipamentos'),
    path('registar_equipamento/', views.registar_equipamento, name='bdii_registar_equipamento'),
    path('vendas_equipamentos/', views.vendas_equipamentos, name='bdii_vendas_equipamentos'),
    path('gestao_clientes/', views.gestao_clientes, name='bdii_gestao_clientes'),
    path('gestao_clientes/fetch_encomendas_cliente/<int:client_id>/',views.fetch_encomendas_cliente, name = 'fetch_encomendas_cliente'),

    path('delete-cliente/<int:cliente_id>/', views.delete_cliente, name='delete_cliente'),
    path('homepage/', views.home, name='home'),
    path('gerar_relatorio_excel/', views.gerar_relatorio_excel, name='gerar_relatorio_excel'),
    path('registo_encomenda/fetch_encomenda_data/<int:encomenda_id>/', views.fetch_encomenda_data, name='fetch_encomenda_data'),
    path('registo_encomenda/guardar_fatura/<int:encomenda_id>/', views.guardar_fatura, name='guardar_fatura'),
    path('registo_encomenda/fetch_guia_data/<int:encomenda_id>/', views.fetch_guia_data, name='fetch_guia_data'),
    path('registo_encomenda/guardar_guia/<int:encomenda_id>/', views.guardar_guia, name='guardar_guia'),
    path('registar_equipamento/fetch_registo_componentes/<int:producao_header_id>/', views.fetch_registo_componentes, name='fetch_registo_componentes'),

    path('vendas_equipamentos/fetch_registo_venda/<str:emailCliente>/',views.fetch_registo_venda, name = 'fetch_registo_venda'),
    path('vendas_equipamentos/fetch_fatura_venda_data/<int:venda_id>/',views.fetch_fatura_venda_data, name = 'fetch_fatura_venda_data'),
    path('vendas_equipamentos/guardar_fatura_cliente/<int:venda_id>/',views.guardar_fatura_cliente, name = 'guardar_fatura_cliente'),
    path('vendas_equipamentos/guardar_guia_fatura/<int:venda_id>/',views.guardar_guia_fatura, name = 'guardar_guia_fatura'),
]

