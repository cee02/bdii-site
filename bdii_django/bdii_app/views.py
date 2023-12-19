from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import connection
import psycopg2
from django.db import OperationalError

def get_database_connection():
    dbname = 'projeto_bdii'
    user = 'postgres'
    password = 'computador123@A'
    port = '5433'

    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=password, port=port)
        return connection
    except OperationalError as e:
        print("OperationalError:", e)
        return None

# Function to close the database connection
def close_database_connection(connection):
    if connection:
        connection.close()

# View functions
def gestao_clientes(request):
    connection = get_database_connection()

    if connection:
        with connection.cursor() as cursor:
            # Use SELECT to execute the stored procedure without fetching any result
            cursor.execute('SELECT get_cliente_data()')
            
            # Commit the transaction to apply changes
            connection.commit()

        close_database_connection(connection)
        return render(request, 'gestao_clientes.html')
    else:
        # Handle the case when the database connection fails
        return render(request, 'error_page.html', {'error_message': 'Failed to connect to the database'})

def login(request):
    return render(request, 'login.html')
def dashboard(request):
    return render(request, 'dashboard.html')

def registo_encomenda(request):
    return render(request, 'registo_encomenda.html')

def get_armazem_data(request):
    with connection.cursor() as cursor:
        # Call the stored procedure
        cursor.callproc('get_armazem_data', [])
        armazem_data = cursor.fetchall()

    context = {
        'armazem_data': armazem_data,
    }

    return render(request, '.html', context)

def registar_equipamento(request):
    return render(request, 'registar_equipamento.html')

def vendas_equipamentos(request):
    return render(request, 'vendas_equipamentos.html')


def producao_equipamentos(request):

     return render(request, 'producao_equipamentos.html')