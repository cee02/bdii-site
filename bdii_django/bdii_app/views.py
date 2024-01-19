from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import connection
import psycopg2
from django.db import OperationalError
from django.http import HttpResponse
import json

def error_page(request, error_message):
    return render(request, 'error_page.html', {'error_message': error_message})

def get_database_connection(username, password):
    # Map user profiles to database configurations
    database_configurations = {
        'aluno3_a': {'dbname': 'projeto_bdii', 'user': 'aluno3_a', 'password': 'aluno', 'port': '5433'},
        'aluno3_b': {'dbname': 'projeto_bdii', 'user': 'aluno3_b', 'password': 'aluno', 'port': '5433'},
        'aluno3_c': {'dbname': 'projeto_bdii', 'user': 'aluno3_c', 'password': 'aluno', 'port': '5433'},
    }

    try:
        # Get the database configurations based on the username
        db_config = database_configurations.get(username)

        if not db_config:
            raise ValueError("Perfil de usuário não reconhecido")

        # Add 'user' and 'password' to the database configurations
        db_config['user'] = username
        db_config['password'] = password

        # Connect to the database using the profile-specific configurations
        connection = psycopg2.connect(
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            port=db_config['port']
        )

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
    username = request.session.get('username')
    password = request.session.get('password')
    print(username)
    print(password)
    connection = get_database_connection(username, password)
    
    user_name = request.session.get('username', 'Guest') # para o nome no menu lateral

    if connection:
        try:
            # Criar um cursor a partir da conexão
            cursor = connection.cursor()

            # Chamar a procedure usando SELECT
            cursor.execute('SELECT * FROM get_cliente_data_function()')

            # Recuperar os resultados da procedure
            results = cursor.fetchall()
            print(results)
            # Fechar o cursor
            cursor.close()

            # Fechar a conexão
            close_database_connection(connection)

            # Passar os resultados para o contexto da renderização
            return render(request, 'gestao_clientes.html', {'clientes': results, 'user_name': user_name})
        except Exception as e:
            # Lidar com exceções, se houver algum problema durante a execução da procedure
            return render(request, 'error_page.html', {'error_message': str(e)})
    else:
        # Lidar com o caso em que a conexão com o banco de dados falha
        return render(request, 'error_page.html', {'error_message': 'Failed to connect to the database'})
    
def producao_equipamentos(request):
    # Obter conexão com o banco de dados
    print("Entrando na view producao_equipamentos")
    username = request.session.get('username')
    password = request.session.get('password')
    print(username)
    print(password)
    connection = get_database_connection(username, password)

    user_name = request.session.get('username', 'Guest') # para o nome no menu lateral
    
    if connection:
        try:
            # Criar um cursor a partir da conexão
            cursor = connection.cursor()

            # Chamar a procedure usando SELECT para a função get_componentes_data_function
            cursor.execute('SELECT * FROM get_componentes_data_function()')

            # Recuperar os resultados da procedure
            componentes_results = cursor.fetchall()
            print("Resultados da função get_componentes_data_function:", componentes_results)

            # Chamar a procedure usando SELECT para a função get_equipamentos_prontos_para_armazenar
            cursor.execute('SELECT * FROM get_equipamentos_prontos_para_armazenar()')

            # Recuperar os resultados da procedure
            equipamentos_results = cursor.fetchall()
            print("Resultados da função get_equipamentos_prontos_para_armazenar:", equipamentos_results)

            # Fechar o cursor
            cursor.close()

            # Fechar a conexão
            close_database_connection(connection)

            # Passar os resultados para o contexto da renderização
            return render(request, 'producao_equipamentos.html', {'componentes': componentes_results, 'equipamentos': equipamentos_results, 'user_name': user_name})
        except Exception as e:
            # Lidar com exceções, se houver algum problema durante a execução da procedure
            return render(request, 'error_page.html', {'error_message': str(e)})
    else:
        # Lidar com o caso em que a conexão com o banco de dados falha
        return render(request, 'error_page.html', {'error_message': 'Failed to connect to the database'})
    

    
def insert_componentes_to_db(username, password, componentes_data):
    try:
        connection = get_database_connection(username, password)

        cursor = connection.cursor()

        cursor.execute('SELECT * FROM inserir_componentes_json(%s)', [json.dumps(componentes_data)])

        connection.commit()

        print("Dados inseridos com sucesso!")

    except OperationalError as e:
        print("OperationalError:", e)
        return HttpResponse("Falha ao inserir dados no banco de dados.", status=500)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def importar_componentes(request):
    # Caminho para o arquivo JSON
    json_file_path = '\Projeto_BDII/bdii-site/bdii_django/bdii_app/componentes.json'

    # Lê o conteúdo do arquivo JSON
    with open(json_file_path, 'r') as file:
        componentes_data = json.load(file)

    # Obtenha as credenciais do usuário da sessão
    username = request.session.get('username')
    password = request.session.get('password')

    # Insira os componentes no banco de dados
    result = insert_componentes_to_db(username, password, componentes_data)

    if isinstance(result, HttpResponse):
        return result

    return HttpResponse("Dados importados com sucesso!")


def delete_cliente(request, cliente_id):
    # Obter conexão com o banco de dados
    username = request.session.get('username')
    password = request.session.get('password')
    print(username)
    print(password)
    connection = get_database_connection(username, password)

    user_name = request.session.get('username', 'Guest') # para o nome no menu lateral

    if connection:
        try:
            # Criar um cursor a partir da conexão
            cursor = connection.cursor()

            cursor.execute('SELECT delete_cliente(%s)', [cliente_id])
            connection.commit()
            # Chamar a procedure usando SELECT
            cursor.execute('SELECT * FROM get_cliente_data_function()')

            # Recuperar os resultados da procedure
            results = cursor.fetchall()
            cursor.close()
            close_database_connection(connection)

            # Passar os resultados para o contexto da renderização
            return render(request, 'gestao_clientes.html', {'clientes': results, 'user_name': user_name})
        except Exception as e:
            # Lidar com exceções, se houver algum problema durante a execução da procedure
            return render(request, 'error_page.html', {'error_message': str(e)})
    else:
        # Lidar com o caso em que a conexão com o banco de dados falha
        return render(request, 'error_page.html', {'error_message': 'Failed to connect to the database'})    

def user_login(request):
    if request.method == 'GET':
        # Get login credentials from the URL or request.GET
        username = request.GET.get('username')
        password = request.GET.get('password')
        
        # Realizar a autenticação (substitua isso pela sua lógica de autenticação)
        if (username == 'aluno3_a' and password == 'aluno') or \
           (username == 'aluno3_b' and password == 'aluno') or \
           (username == 'aluno3_c' and password == 'aluno'):
            print(username, password)
            request.session['username'] = username
            request.session['password'] = password

            # Credenciais válidas, redirecionar para o dashboard
            return redirect('/dashboard')
            
        else:
            # Credenciais inválidas, renderizar a página de login com uma mensagem de erro
            return render(request, 'login.html', {'error_message': 'Credenciais inválidas. Tente novamente.'})
    else:
        # Se o método não for GET, renderizar a página de login
        return render(request, 'login.html')

def logout(request):
    logout(request)
    return render(request, 'login.html')

def dashboard(request):
    user_name = request.session.get('username', 'Guest') # para o nome no menu lateral
    importar_componentes(request)
    return render(request, 'dashboard.html', {'user_name': user_name})

def registo_encomenda(request):
    user_name = request.session.get('username', 'Guest') # para o nome no menu lateral
    return render(request, 'registo_encomenda.html', {'user_name': user_name})

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
    user_name = request.session.get('username', 'Guest') # para o nome no menu lateral
    return render(request, 'registar_equipamento.html', {'user_name': user_name})

def vendas_equipamentos(request):
    user_name = request.session.get('username', 'Guest') # para o nome no menu lateral
    return render(request, 'vendas_equipamentos.html', {'user_name': user_name})

def registar_equipamento(request): # listar componentes
    # Obter conexão com o banco de dados
    user_name = request.session.get('username', 'Guest') 
    print("Entrando na view registo_equipamentos")
    username = request.session.get('username')
    password = request.session.get('password')
    print(username)
    print(password)
    connection = get_database_connection(username, password)

    user_name = request.session.get('username', 'Guest') # para o nome no menu lateral
    
    if connection:
        try:
            # Criar um cursor a partir da conexão
            cursor = connection.cursor()

            # Chamar a procedure usando SELECT para a função get_componentes_data_function
            cursor.execute('SELECT * FROM get_componentes_data_function()')

            # Recuperar os resultados da procedure
            componentes_results = cursor.fetchall()
            print("Resultados da função get_componentes_data_function:", componentes_results)

            # Chamar a procedure usando SELECT para a função get_equipamentos_prontos_para_armazenar
            cursor.execute('SELECT * FROM get_equipamentos_prontos_para_armazenar()')

            # Recuperar os resultados da procedure
            equipamentos_results = cursor.fetchall()
            print("Resultados da função get_equipamentos_prontos_para_armazenar:", equipamentos_results)

            # Fechar o cursor
            cursor.close()

            # Fechar a conexão
            close_database_connection(connection)

            # Passar os resultados para o contexto da renderização
            return render(request, 'registar_equipamento.html', {'componentes': componentes_results, 'equipamentos': equipamentos_results, 'user_name': user_name})
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