import os
import psycopg2
from pymongo import MongoClient
import biohashing
import time
import psutil
import csv

# --- CONFIGURAÇÃO DOS BANCOS DE DADOS ---

# Conexão com PostgreSQL
conn_pg = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="******", # Senha ocultada por segurança
    client_encoding='LATIN1'
)
cursor_pg = conn_pg.cursor()

# Conexão com MongoDB
client_mongo = MongoClient('mongodb://localhost:27017/')
db_mongo = client_mongo['tcc_db']
collection_mongo = db_mongo['templates']

# --- DEFINIÇÃO DAS FUNÇÕES ---

def setup_postgresql():
    """Cria a tabela no PostgreSQL se ela ainda não existir."""
    comando_sql = """
    CREATE TABLE IF NOT EXISTS templates_pg (
        id SERIAL PRIMARY KEY,
        caminho_imagem TEXT,
        biocode TEXT
    );
    """
    cursor_pg.execute(comando_sql)
    conn_pg.commit()
    print("Tabela 'templates_pg' no PostgreSQL está pronta.")

def inserir_postgres(caminho_imagem, biocode):
    """Insere um novo registro na tabela do PostgreSQL."""
    biocode_str = "".join(map(str, biocode))
    cursor_pg.execute(
        "INSERT INTO templates_pg (caminho_imagem, biocode) VALUES (%s, %s)",
        (caminho_imagem, biocode_str)
    )
    conn_pg.commit()

def inserir_mongodb(caminho_imagem, biocode):
    """Insere um novo documento na coleção do MongoDB."""
    biocode_list = biocode.tolist()
    documento = {
        'caminho_imagem': caminho_imagem,
        'biocode': biocode_list
    }
    collection_mongo.insert_one(documento)

def ler_postgres(caminho_imagem, biocode):
    """Busca por um biocode específico no PostgreSQL."""
    biocode_str = "".join(map(str, biocode))
    cursor_pg.execute(
        "SELECT id FROM templates_pg WHERE biocode = %s LIMIT 1;",
        (biocode_str,)
    )
    cursor_pg.fetchone()

def ler_mongodb(caminho_imagem, biocode):
    """Busca por um biocode específico no MongoDB."""
    biocode_list = biocode.tolist()
    collection_mongo.find_one({'biocode': biocode_list})    

def medir_desempenho(funcao_alvo, caminho_imagem, biocode):
    """Executa uma função alvo e mede o tempo, CPU e memória gastos."""
    start_time = time.time()
    # Captura o uso de CPU e memória
    cpu_antes = psutil.cpu_percent(interval=None)
    mem_antes = psutil.virtual_memory().percent

    # Executa a função que queremos medir
    funcao_alvo(caminho_imagem, biocode)

    # Captura as métricas DEPOIS da execução
    end_time = time.time()
    cpu_depois = psutil.cpu_percent(interval=None)
    mem_depois = psutil.virtual_memory().percent
    tempo_decorrido = end_time - start_time
    
    # Retorna os resultados em um formato organizado
    return {
        "tempo_s": tempo_decorrido,
        "cpu_percent": cpu_depois,
        "mem_percent": mem_depois
    }

# --- LÓGICA PRINCIPAL ---

# Prepara a tabela e limpa os dados de testes anteriores
setup_postgresql()
collection_mongo.delete_many({}) # Limpa a coleção do MongoDB para um novo teste

# Defina o caminho para a pasta principal de datasets
caminho_datasets = r'dataset/FVC2004'

seed_usuario = 123
print("\nIniciando a primeira rodada de testes...")

# Preparando o arquivo CSV para salvar os resultados
nome_arquivo_csv = 'resultados_finais_massivos.csv'
with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    # Adicionamos a coluna "operacao" ao cabeçalho
    writer.writerow(['imagem', 'operacao', 'plataforma', 'tempo_s', 'cpu_percent', 'mem_percent'])

    contador = 0

    for raiz, diretorios, arquivos in os.walk(caminho_datasets):
        for arquivo in arquivos:
            if arquivo.endswith(".tif"):
                caminho_completo = os.path.join(raiz, arquivo)
                print(f"Testando com: {caminho_completo}")

                vetor = biohashing.extrair_vetor_da_imagem(caminho_completo)
                if vetor is not None:
                    biocode = biohashing.gerar_biocode(vetor, seed_usuario)
                    if biocode is not None:
                        # --- TESTE DE INSERÇÃO ---
                        res_pg_ins = medir_desempenho(inserir_postgres, caminho_completo, biocode)
                        writer.writerow([caminho_completo, 'insercao', 'PostgreSQL', res_pg_ins['tempo_s'], res_pg_ins['cpu_percent'], res_pg_ins['mem_percent']])

                        res_mongo_ins = medir_desempenho(inserir_mongodb, caminho_completo, biocode)
                        writer.writerow([caminho_completo, 'insercao', 'MongoDB', res_mongo_ins['tempo_s'], res_mongo_ins['cpu_percent'], res_mongo_ins['mem_percent']])

                        # --- TESTE DE LEITURA (VERIFICAÇÃO 1:1) ---
                        res_pg_read = medir_desempenho(ler_postgres, caminho_completo, biocode)
                        writer.writerow([caminho_completo, 'leitura_1_1', 'PostgreSQL', res_pg_read['tempo_s'], res_pg_read['cpu_percent'], res_pg_read['mem_percent']])

                        res_mongo_read = medir_desempenho(ler_mongodb, caminho_completo, biocode)
                        writer.writerow([caminho_completo, 'leitura_1_1', 'MongoDB', res_mongo_read['tempo_s'], res_mongo_read['cpu_percent'], res_mongo_read['mem_percent']])
                        
                        contador += 1

# Fecha as conexões com os bancos de dados no final
cursor_pg.close()
conn_pg.close()
client_mongo.close()

print(f"\nProcesso concluído! Os resultados de {contador} imagens foram salvos em '{nome_arquivo_csv}'.")
