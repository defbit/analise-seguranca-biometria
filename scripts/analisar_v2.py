import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

def main():
    print("--- INICIANDO ANÁLISE ESTATÍSTICA (MÉDIA + DESVIO PADRÃO) ---")

    # 1. DEFINIR DIRETÓRIOS
    # Descobre onde este script está salvo
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    
    # Define que a pasta de resultados é 'vizinha' à pasta do script (sobe um nível e entra em 'resultados')
    # Estrutura esperada:
    #   /projeto
    #       /scripts (script aqui)
    #       /resultados (dados aqui)
    diretorio_dados = os.path.join(os.path.dirname(diretorio_script), "resultados")

    print(f"-> Buscando dados na pasta: {diretorio_dados}")

    if not os.path.exists(diretorio_dados):
        print(f"ERRO: A pasta '{diretorio_dados}' não foi encontrada.")
        return

    # 2. BUSCAR ARQUIVOS
    padrao_busca = os.path.join(diretorio_dados, "resultados_*.csv")
    arquivos = glob.glob(padrao_busca)

    if not arquivos:
        print("ERRO: Nenhum arquivo 'resultados_*.csv' encontrado na pasta de resultados.")
        return

    print(f"-> Encontrados {len(arquivos)} arquivos para análise.")

    # 3. CARREGAR E CONSOLIDAR
    lista_dfs = []
    for arquivo in arquivos:
        try:
            df_temp = pd.read_csv(arquivo)
            lista_dfs.append(df_temp)
        except Exception as e:
            print(f"Aviso: Erro ao ler {os.path.basename(arquivo)}: {e}")

    if not lista_dfs:
        print("Nenhum dado válido carregado.")
        return

    df_completo = pd.concat(lista_dfs, ignore_index=True)
    
    # Garante que a coluna de tempo existe
    if 'tempo_s' not in df_completo.columns:
        # Tenta achar variante
        cols = [c for c in df_completo.columns if 'tempo' in c.lower()]
        if cols:
            coluna_tempo = cols[0]
        else:
            print("ERRO: Coluna de tempo não encontrada.")
            return
    else:
        coluna_tempo = 'tempo_s'

    # 4. CÁLCULO ESTATÍSTICO
    print("\nCalculando estatísticas...")
    tabela_estatistica = df_completo.groupby(['plataforma', 'operacao'])[coluna_tempo].agg(['mean', 'std'])
    tabela_estatistica = tabela_estatistica.rename(columns={'mean': 'Tempo Médio (s)', 'std': 'Desvio Padrão (s)'})
    
    print("-" * 80)
    print(tabela_estatistica)
    print("-" * 80)

    # Salvar Tabela na pasta RESULTADOS
    caminho_tabela = os.path.join(diretorio_dados, 'tabela_estatistica_final.csv')
    tabela_estatistica.to_csv(caminho_tabela)
    print(f"-> Tabela salva em: {caminho_tabela}")

    # 5. GERAÇÃO DOS BOXPLOTS
    print("\nGerando Gráficos Boxplot...")
    sns.set(style="whitegrid")

    # --- Boxplot Inserção ---
    try:
        plt.figure(figsize=(10, 6))
        dados_insercao = df_completo[df_completo['operacao'] == 'insercao']
        
        sns.boxplot(x='plataforma', y=coluna_tempo, data=dados_insercao, showfliers=False, palette="Set2")
        
        plt.title('Variabilidade do Tempo de Inserção (Boxplot)', fontsize=14)
        plt.ylabel('Tempo (segundos)', fontsize=12)
        plt.xlabel('Plataforma', fontsize=12)
        plt.yscale('log') 
        
        caminho_img_insercao = os.path.join(diretorio_dados, 'boxplot_insercao.png')
        plt.tight_layout()
        plt.savefig(caminho_img_insercao, dpi=300)
        print(f"-> Gráfico salvo em: {caminho_img_insercao}")
        plt.close()
    except Exception as e:
        print(f"Erro no gráfico de inserção: {e}")

    # --- Boxplot Leitura ---
    try:
        plt.figure(figsize=(10, 6))
        # Filtra leitura (ajuste flexível para 'leitura' ou 'leitura_1_1')
        dados_leitura = df_completo[df_completo['operacao'].str.contains('leitura')]
        
        sns.boxplot(x='plataforma', y=coluna_tempo, data=dados_leitura, showfliers=False, palette="Set2")
        
        plt.title('Variabilidade do Tempo de Leitura (Boxplot)', fontsize=14)
        plt.ylabel('Tempo (segundos)', fontsize=12)
        plt.xlabel('Plataforma', fontsize=12)
        
        caminho_img_leitura = os.path.join(diretorio_dados, 'boxplot_leitura.png')
        plt.tight_layout()
        plt.savefig(caminho_img_leitura, dpi=300)
        print(f"-> Gráfico salvo em: {caminho_img_leitura}")
        plt.close()
    except Exception as e:
        print(f"Erro no gráfico de leitura: {e}")

    print("\n--- CONCLUÍDO ---")

if __name__ == "__main__":
    main()