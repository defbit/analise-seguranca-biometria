import pandas as pd
import glob

# CONFIGURAÇÃO
# Lista com o nome exato dos arquivos de resultados
nomes_dos_arquivos = [
    'resultados_bancos_de_dados.csv', # Contém os dados de PostgreSQL e MongoDB
    'resultados_blockchain_DB1.csv',
    'resultados_blockchain_DB2.csv',
    'resultados_blockchain_DB3.csv',
    'resultados_blockchain_DB4.csv'
]

print(f"Analisando os seguintes arquivos: {nomes_dos_arquivos}")

# --- PASSO 1: CONSOLIDAR OS DADOS ---
lista_de_dataframes = []
for arquivo in nomes_dos_arquivos:
    try:
        df = pd.read_csv(arquivo)
        lista_de_dataframes.append(df)
    except FileNotFoundError:
        print(f"AVISO: O arquivo '{arquivo}' não foi encontrado e será ignorado.")

if lista_de_dataframes:
    dados_completos = pd.concat(lista_de_dataframes, ignore_index=True)
    
    # --- PASSO 2: CALCULAR AS MÉTRICAS ---
    colunas_numericas = ['plataforma', 'operacao', 'tempo_s', 'cpu_percent', 'mem_percent']
    dados_para_analise = dados_completos[colunas_numericas]

    tabela_resumo = dados_para_analise.groupby(['plataforma', 'operacao']).mean()
    
    # --- PASSO 3: EXIBIR E SALVAR O RESULTADO FINAL ---
    print("\n--- Tabela Resumo da Análise de Desempenho ---")
    
    pd.set_option('display.float_format', lambda x: f'{x:.4f}')
    
    print(tabela_resumo)

    # Salva a tabela resumo em um novo arquivo CSV
    nome_arquivo_final = 'Tabela_Resumo_Final.csv'
    tabela_resumo.to_csv(nome_arquivo_final)
    
    print(f"\n[SUCESSO] A Tabela Resumo também foi salva no arquivo: '{nome_arquivo_final}'")

else:
    print("Nenhum dado foi carregado. A análise não pôde ser concluída.")
