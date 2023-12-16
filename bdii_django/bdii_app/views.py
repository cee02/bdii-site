from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Componente, Cliente

def login(request):
    return render(request, 'login.html')
def dashboard(request):
    return render(request, 'dashboard.html')

def registo_encomenda(request):
    return render(request, 'registo_encomenda.html')

def producao_equipamentos(request):
    # Obter os componentes em stock usando a view do PostgreSQL
    componentes_em_stock = Componente.objects.raw('SELECT * FROM read_componentes_em_stock;')

    # Passar os componentes para o contexto
    context = {'componentes_em_stock': componentes_em_stock}

    # Renderizar a página com a lista de componentes em stock
    return render(request, 'producao_equipamentos.html', context)

def gestao_clientes(request):
    clientes = Cliente.objects.all()  # Consulta todos os clientes
    print('Clientes:', clientes) #LOg temporário
    return render(request, 'gestao_clientes.html', {'clientes': clientes})

def registar_equipamento(request):
    return render(request, 'registar_equipamento.html')

def vendas_equipamentos(request):
    return render(request, 'vendas_equipamentos.html')


