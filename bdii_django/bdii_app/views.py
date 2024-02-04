from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import connection
import psycopg2
from django.db import OperationalError
from django.http import HttpResponse
import json
from django.db import connections
from django.db import transaction
import pandas as pd
import os
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse


def error_page(request, error_message):
    return render(request, 'error_page.html', {'error_message': error_message})

def get_database_connection(username, password):
    # Map user profiles to database configurations
    database_configurations = {
        'aluno3_a': {'dbname': 'projeto_bdii', 'user': 'aluno3_a', 'password': 'aluno', 'port': '5432'},
        'aluno3_b': {'dbname': 'projeto_bdii', 'user': 'aluno3_b', 'password': 'aluno', 'port': '5432'},
        'aluno3_c': {'dbname': 'projeto_bdii', 'user': 'aluno3_c', 'password': 'aluno', 'port': '5432'},
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
    username = request.session.get('username')
    password = request.session.get('password')
    connection = get_database_connection(username, password)

    user_name = request.session.get('username', 'Guest')  # para o nome no menu lateral
    
    if connection:
        try:
            result = None 

            if request.method == 'POST':  # Verificar se o formulário foi submetido
                # Obter os valores do formulário
                componente_ids = request.POST.get('component_id')
                quantidade_componente = request.POST.get('quantidade_componente')
                tipooperacao = request.POST.get('tipo_operacao')
                mao_obra = request.POST.get('mao_de_obra')

                print('Component ID:', componente_ids)
                print('Tipo de Operação:', tipooperacao)
                print('Mão de Obra:', mao_obra)

                # Chamar a função para inserir na ficha de produção
                with connection.cursor() as cursor:
                    try:
                        # Convert the list of strings to a list of integers
                        componente_ids = [int(id) for id in componente_ids.split(',')]

                        cursor.execute('INSERT INTO ProducaoHeader DEFAULT VALUES RETURNING Id')
                        producao_header_id = cursor.fetchone()[0]

                        cursor.execute('SELECT * FROM insert_componentes_ficha_producao(%s, %s, %s, %s, %s)',
                            [componente_ids, 1, int(tipooperacao), int(mao_obra), producao_header_id]
                        )    
                        print('insert_componentes_ficha_producao executed')
                        result = cursor.fetchone()
                        connection.commit()
                    

                        # Print the data directly after insertion
                        cursor.execute('SELECT * FROM ComponentesFichaProducao')
                        print('Data after insertion:', cursor.fetchall())

                    except Exception as e:
                        print('Error during insert:', e)

            with connection.cursor() as cursor:
                # Chamar a procedure usando SELECT para a função get_componentes_data_function
                cursor.execute('SELECT * FROM get_componentes_data_function()')

                # Recuperar os resultados da procedure
                componentes_results = cursor.fetchall()

                # Chamar a procedure usando SELECT para a função get_equipamentos_prontos_para_armazenar
                cursor.execute('SELECT * FROM get_equipamentos_prontos_para_armazenar()')

                # Recuperar os resultados da procedure
                equipamentos_results = cursor.fetchall()

                # Buscar dados adicionais
                cursor.execute("SELECT * FROM vw_tipo_operacao")
                tipo_operacao_list = cursor.fetchall()

                cursor.execute("SELECT * FROM vw_mao_obra")
                mao_obra_list = cursor.fetchall()

            # Fechar a conexão
            close_database_connection(connection)

            # Passar os resultados para o contexto da renderização
            return render(request, 'producao_equipamentos.html', {'componentes': componentes_results, 'equipamentos': equipamentos_results, 'user_name': user_name,'tipo_operacao': tipo_operacao_list,'mao_de_obra': mao_obra_list, 'result': result})
        except Exception as e:
            # Lidar com exceções, rolar a transação de volta se necessário

            return render(request, 'error_page.html', {'error_message': str(e)})
    else:
        # Lidar com o caso em que a conexão com o banco de dados falha
        return render(request, 'error_page.html', {'error_message': 'Failed to connect to the database'})


def insert_componentes_to_db(username, password, componentes_data):
    try:
        connection = get_database_connection(username, password)

        cursor = connection.cursor()
        print("JSON Data:", componentes_data)
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
    json_file_path = 'D:\\Universidade\\BDII\\Projeto_BDII\\bdii-site\\bdii_django\\bdii_app\\componentes.json'
    #json_file_path = '\Projeto_BDII/bdii-site/bdii_django/bdii_app/componentes.json'

    try:
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
        print("Dados importados com sucesso!")

    except Exception as e:
        # Handle exceptions related to file reading or database insertion
        print(f"An error occurred during import: {str(e)}")

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
    if request.method == 'POST':
        # Get login credentials from the POST data
        username = request.POST.get('username')
        password = request.POST.get('password')
        
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
        # Se o método não for POST, renderizar a página de login
        return render(request, 'login.html')

def logout(request):
    logout(request)
    return render(request, 'login.html')

def dashboard(request):
    user_name = request.session.get('username', 'Guest') # para o nome no menu lateral
    if user_name == 'aluno3_c':
        return redirect('home')
    
    try:
        importar_componentes(request)  # A chamar o IMPORTAR COMPONENTES

        with connections['default'].cursor() as cursor:
            # Vai buscar os componentes que entraram recentemente
            cursor.execute("SELECT * FROM componente_entrada_stock_recente")
            componente_entrada_stock_recente = cursor.fetchall()
        
            # Vai buscar os equipamentos que entraram recentemente
            cursor.execute("SELECT * FROM equipamento_entrada_stock_recente")
            equipamento_entrada_stock_recente = cursor.fetchall()

            # Vai buscar os componentes que sairam recentemente
            cursor.execute("SELECT * FROM componente_saida_stock_recente")
            componente_saida_stock_recente = cursor.fetchall()

            # Vai buscar os equipamentos que sairam recentemente
            cursor.execute("SELECT * FROM equipamento_saida_stock_recente")
            equipamento_saida_stock_recente = cursor.fetchall()

            # Vai buscar os componentes em low stock
            cursor.execute("SELECT * FROM low_stock_components")
            low_stock_components_data = cursor.fetchall()

            # Vai buscar os componentes em low stock
            cursor.execute("SELECT * FROM view_meses_anos_componentearmazem")
            view_meses_anos_componentearmazem = cursor.fetchall()

    except Exception as e:
        # Handle exceptions (e.g., database connection error, file not found, etc.)
        print(f"An error occurred: {str(e)}")
        low_stock_components_data = []

    return render(request, 'dashboard.html', {'user_name': user_name, 'componente_entrada_stock_recente': componente_entrada_stock_recente,
                                              'equipamento_entrada_stock_recente': equipamento_entrada_stock_recente,'componente_saida_stock_recente': componente_saida_stock_recente,
                                              'equipamento_saida_stock_recente': equipamento_saida_stock_recente, 'low_stock_components_data': low_stock_components_data,
                                              'view_meses_anos_componentearmazem': view_meses_anos_componentearmazem})

   

def registo_encomenda(request):
    fornecedores = obter_fornecedores()
    componentes = obter_componentes()
    idencomenda = obter_encomendas()

    if request.method == 'POST':
        componentes_list = request.POST.getlist('componente[]')
        quantidades_list = request.POST.getlist('quantidade[]')
        fornecedor_id = request.POST.get('fornecedor_id')
        print (componentes_list)
        with connection.cursor() as cursor:
            try:
                #
                cursor.execute('INSERT INTO Encomenda_componentesHeader DEFAULT VALUES RETURNING Id')
                encomenda_header_id = cursor.fetchone()[0]

                # Convert the component IDs to a list of integers
                componentes_array = [int(componente) for componente in componentes_list]
                quantidades_array = [int(quantidade) for quantidade in quantidades_list]

                cursor.execute("SELECT insert_componentes_pedido_compra(%s, %s, %s, %s)",
                            [componentes_array, quantidades_array, int(fornecedor_id), encomenda_header_id])
        
                # Commit the changes
                connection.commit()

            except Exception as e:
                # Rollback the transaction if an exception occurs
                connection.rollback()
                return render(request, 'error_page.html', {'error_message': str(e)})

    user_name = request.session.get('username', 'Guest')
    return render(request, 'registo_encomenda.html', {'user_name': user_name, 'fornecedores': fornecedores, 'componentes': componentes, 'idencomenda': idencomenda})

def fetch_encomenda_data(request, encomenda_id):
    try:
        with connections['default'].cursor() as cursor:
            # Vai buscar o nome do fornecedor
            cursor.execute("SELECT * FROM nomeFornecedorDadoIDenc(%s)", [int(encomenda_id)])
            nomeFornecedor = cursor.fetchall()
        
            # Vai buscar a data da encomenda
            cursor.execute("SELECT * FROM datahoraDadoIdEnc(%s)", [int(encomenda_id)])
            dataHora = cursor.fetchall()

            # Vai buscar os componentes que sairam recentemente
            cursor.execute("SELECT * FROM calcular_valor_total_encomenda(%s)", [int(encomenda_id)])
            valorTotal = cursor.fetchall()

            # Vai buscar as informações dos componentes da encomenda
            cursor.execute("SELECT * FROM obter_info_componentes_encomenda(%s)", [int(encomenda_id)])
            componentes_info = cursor.fetchall()

            data = {
            'nomeFornecedor': nomeFornecedor,
            'dataHora': dataHora,  # Formato para datetime-local
            'valorTotal': valorTotal,
            'componentes_info': componentes_info,
            }
        return JsonResponse(data)
    
    except Exception as e:
        # Handle exceptions (e.g., database connection error, file not found, etc.)
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'Encomenda não encontrada'}, status=404)



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
    user_name = request.session.get('username', 'Guest')
    componentes = []

    producao_header_id = request.POST.get('encomenda_id', None)
    print('producao_header_id:', producao_header_id)
    if producao_header_id:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM vw_componentes_by_producao_header WHERE id_producao_header = %s",
                    [producao_header_id]
                )
                columns = [col[0] for col in cursor.description]
                componentes = [dict(zip(columns, row)) for row in cursor.fetchall()]
                print('Componentes:', componentes)

    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM vw_componentes_ProducaoHeader")
        encomenda_ids = [row[0] for row in cursor.fetchall()]

    return render(request, 'registar_equipamento.html', {'user_name': user_name, 'encomenda_ids': encomenda_ids, 'componentes': componentes})


def vendas_equipamentos(request):
    user_name = request.session.get('username', 'Guest') # para o nome no menu lateral
    return render(request, 'vendas_equipamentos.html', {'user_name': user_name})

def home(request):
    
    user_name = request.session.get('username', 'Guest')
    return render(request, 'homepage.html', {'user_name': user_name})
    
def fazerregisto_equipamento(request): #registar equipamento (ainda nao pinta)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registar_equipamento') 
    else:
        form = EquipamentoForm()

    return render(request, 'registar_equipamento.html', {'form': form})

def gerar_relatorio_excel(request):
    # Obtém o mês e ano selecionados no formulário
    mes_ano_selecionado = request.GET.get('mesAno')
    print(f"Valor data: {mes_ano_selecionado}")
    # Verifica se o mês e ano foram fornecidos corretamente
    if not mes_ano_selecionado or '-' not in mes_ano_selecionado:
        return HttpResponse("O mês não foi selecionado corretamente na solicitação.")

    # Divide o valor do formulário em mês e ano
    try:
        mes, ano = mes_ano_selecionado.split('-')
        print(f"Valor mes: {mes}")
        print(f"Valor ano: {ano}")
        # Verifica se o mês é um número válido
        if not mes.isdigit():
            raise ValueError("Formato de mês inválido.")
    except ValueError as e:
        return HttpResponse(str(e))

    # Consulta os componentes que entraram e saíram no mês e ano selecionados
    #query_entrada = "SELECT * FROM componentearmazem WHERE EXTRACT(MONTH FROM data_entrada) = %s AND EXTRACT(YEAR FROM data_entrada) = %s"
    query_entrada_componentes = f"SELECT * FROM view_componentes_armazem_entrada WHERE EXTRACT(MONTH FROM data_entrada) = {mes} AND EXTRACT(YEAR FROM data_entrada) = {ano}"

    query_saida_componentes = f"SELECT * FROM view_componentes_armazem_saida WHERE EXTRACT(MONTH FROM data_saida) = {mes} AND EXTRACT(YEAR FROM data_saida) = {ano}"

    # Define a variável excel_file_path
    # Define o caminho para a pasta "Downloads" do usuário atual
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Define a variável excel_file_path
    excel_file_path = os.path.join(downloads_path, f'relatorio_{mes}-{ano}.xlsx')

    # Garante que o diretório exista antes de salvar o arquivo
    os.makedirs(os.path.dirname(excel_file_path), exist_ok=True)

    try:
        with connections['default'].cursor() as cursor:
            cursor.execute(query_entrada_componentes)
            componente_entrada_data = cursor.fetchall()

            cursor.execute(query_saida_componentes)
            componente_saida_data = cursor.fetchall()

        # Cria DataFrames com os resultados
      

        df_entrada = pd.DataFrame(componente_entrada_data, columns=['Nome', 'Preço', 'Quantidade', 'Data', 'Armazem'])
        df_saida = pd.DataFrame(componente_saida_data, columns=['Nome', 'Preço', 'Quantidade', 'Data','Armazem'])
        df_entrada['Tipo Movimento'] = 'Entrada'
        df_saida['Tipo Movimento'] = 'Saída'

        # Concatena os DataFrames
        df_result = pd.concat([df_entrada, df_saida])

        # Converte o DataFrame para um arquivo Excel
        df_result.to_excel(excel_file_path, index=False)

        # Retorna o arquivo Excel como resposta HTTP
        with open(excel_file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename=relatorio_{mes}-{ano}.xlsx'

        return response

    except Exception as e:
        # Trate exceções conforme necessário
        print(f"An error occurred: {str(e)}")
        print(f"Query Saída: {query_saida_componentes}")
        print(f"Excel File Path: {excel_file_path}")
        return HttpResponse("Erro ao gerar o relatório Excel.")

    finally:
        # Garante que o arquivo seja fechado, mesmo se ocorrer uma exceção
        if os.path.exists(excel_file_path):
            os.remove(excel_file_path)

def obter_fornecedores():
    with connection.cursor() as cursor:
        #cursor.execute("SELECT id, nome FROM fornecedor")
        cursor.execute("SELECT * FROM dados_fornecedor")
        fornecedores = cursor.fetchall()

    return fornecedores

def obter_componentes():
    with connection.cursor() as cursor:
        #cursor.execute("SELECT id, nome FROM componentes")
        cursor.execute("SELECT * FROM dados_componentes")
        componentes = cursor.fetchall()

    return componentes

def obter_encomendas():
    with connection.cursor() as cursor:
        #cursor.execute("SELECT id,  FROM encomenda")
        cursor.execute("SELECT * FROM id_encomenda")
        idencomenda = cursor.fetchall()

    return idencomenda
