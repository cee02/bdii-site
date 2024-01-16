from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import connection
import psycopg2
from django.db import OperationalError

def error_page(request, error_message):
    return render(request, 'error_page.html', {'error_message': error_message})

def get_database_connection(user_type):
    # Coloquem os users com as mesmas credenciais
    if user_type == 'aluno3_a':     #admin
        dbname = 'projeto_bdii'
        user = 'aluno3_a'
        password = 'aluno'
        port = '5433'
    elif user_type == 'aluno3_b':   #gestor
        dbname = 'projeto_bdii'
        user = 'aluno3_b'
        password = 'aluno'
        port = '5433'
    elif user_type == 'aluno3_c':   #user
        dbname = 'projeto_bdii'
        user = 'aluno3_c'
        password = 'aluno'
        port = '5433'
    else:
        # Condição padrão ou erro, dependendo dos requisitos do seu aplicativo
        raise ValueError("User não reconhecido")
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
    # Obter conexão com o banco de dados
    connection = get_database_connection(user_type='aluno3_a')

    if connection:
        try:
            # Criar um cursor a partir da conexão
            cursor = connection.cursor()

            # Chamar a procedure usando SELECT
            cursor.callproc('get_cliente_data_function')

            # Recuperar os resultados da procedure
            results = cursor.fetchall()
            print(results)
            # Fechar o cursor
            cursor.close()

            # Fechar a conexão
            close_database_connection(connection)

            # Passar os resultados para o contexto da renderização
            return render(request, 'gestao_clientes.html', {'clientes': results})
        except Exception as e:
            # Lidar com exceções, se houver algum problema durante a execução da procedure
            return render(request, 'error_page.html', {'error_message': str(e)})
    else:
        # Lidar com o caso em que a conexão com o banco de dados falha
        return render(request, 'error_page.html', {'error_message': 'Failed to connect to the database'})
    
def producao_equipamentos(request):
    # Obter conexão com o banco de dados
    print("Entrando na view producao_equipamentos")
    connection = get_database_connection()
    if connection:
        try:
            # Criar um cursor a partir da conexão
            cursor = connection.cursor()

            # Chamar a procedure usando SELECT para a função get_componentes_data_function
            cursor.callproc('get_componentes_data_function')

            # Recuperar os resultados da procedure
            componentes_results = cursor.fetchall()
            print("Resultados da função get_componentes_data_function:", componentes_results)

            # Chamar a procedure usando SELECT para a função get_equipamentos_prontos_para_armazenar
            cursor.callproc('get_equipamentos_prontos_para_armazenar')

            # Recuperar os resultados da procedure
            equipamentos_results = cursor.fetchall()
            print("Resultados da função get_equipamentos_prontos_para_armazenar:", equipamentos_results)

            # Fechar o cursor
            cursor.close()

            # Fechar a conexão
            close_database_connection(connection)

            # Passar os resultados para o contexto da renderização
            return render(request, 'producao_equipamentos.html', {'componentes': componentes_results, 'equipamentos': equipamentos_results})
        except Exception as e:
            # Lidar com exceções, se houver algum problema durante a execução da procedure
            return render(request, 'error_page.html', {'error_message': str(e)})
    else:
        # Lidar com o caso em que a conexão com o banco de dados falha
        return render(request, 'error_page.html', {'error_message': 'Failed to connect to the database'})

def delete_cliente(request, cliente_id):
    # Obter conexão com o banco de dados
    connection = get_database_connection(user_type='aluno3_a')

    if connection:
        try:
            # Criar um cursor a partir da conexão
            cursor = connection.cursor()

            cursor.callproc('delete_cliente', [cliente_id])
            connection.commit()
            # Chamar a procedure usando SELECT
            cursor.callproc('get_cliente_data_function')

            # Recuperar os resultados da procedure
            results = cursor.fetchall()
            cursor.close()
            close_database_connection(connection)

            # Passar os resultados para o contexto da renderização
            return render(request, 'gestao_clientes.html', {'clientes': results})
        except Exception as e:
            # Lidar com exceções, se houver algum problema durante a execução da procedure
            return render(request, 'error_page.html', {'error_message': str(e)})
    else:
        # Lidar com o caso em que a conexão com o banco de dados falha
        return render(request, 'error_page.html', {'error_message': 'Failed to connect to the database'})    


def user_login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'login.html')

def dashboard(request):
    user_name = request.user.username
    return render(request, 'dashboard.html', {'user_name': user_name})

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

def registar_equipamento(request): # listar componentes
    # Obter conexão com o banco de dados
    print("Entrando na view registo_equipamentos")
    connection = get_database_connection()
    if connection:
        try:
            # Criar um cursor a partir da conexão
            cursor = connection.cursor()

            # Chamar a procedure usando SELECT para a função get_componentes_data_function
            cursor.callproc('get_componentes_data_function')

            # Recuperar os resultados da procedure
            componentes_results = cursor.fetchall()
            print("Resultados da função get_componentes_data_function:", componentes_results)

            # Chamar a procedure usando SELECT para a função get_equipamentos_prontos_para_armazenar
            cursor.callproc('get_equipamentos_prontos_para_armazenar')

            # Recuperar os resultados da procedure
            equipamentos_results = cursor.fetchall()
            print("Resultados da função get_equipamentos_prontos_para_armazenar:", equipamentos_results)

            # Fechar o cursor
            cursor.close()

            # Fechar a conexão
            close_database_connection(connection)

            # Passar os resultados para o contexto da renderização
            return render(request, 'registar_equipamento.html', {'componentes': componentes_results, 'equipamentos': equipamentos_results})
        except Exception as e:
            # Lidar com exceções, se houver algum problema durante a execução da procedure
            return render(request, 'error_page.html', {'error_message': str(e)})
    else:
        # Lidar com o caso em que a conexão com o banco de dados falha
        return render(request, 'error_page.html', {'error_message': 'Failed to connect to the database'})
    
def fazerregisto_equipamento(request): #registar equipamento (ainda nao pinta)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registar_equipamento') 
    else:
        form = EquipamentoForm()

    return render(request, 'registar_equipamento.html', {'form': form})