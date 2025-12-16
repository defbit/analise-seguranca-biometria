import os
import biohashing
import time
import psutil
import csv
import numpy as np  
from web3 import Web3

# --- 1. CONFIGURAÇÃO DA CONEXÃO COM GANACHE E SMART CONTRACT ---

# Conexão com a blockchain local (Ganache)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
# Define a primeira conta do Ganache como a conta padrão para enviar transações
w3.eth.default_account = w3.eth.accounts[0]

# valores obtidos do Remix IDE
contract_address = '0x7cd8063D19F8B66dc3fbDb45C7DA0f156c7DF18A'
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "biocodes",
		"outputs": [
			{
				"internalType": "bytes",
				"name": "",
				"type": "bytes"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes",
				"name": "novoBiocode",
				"type": "bytes"
			}
		],
		"name": "guardarBiocode",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "lerBiocode",
		"outputs": [
			{
				"internalType": "bytes",
				"name": "",
				"type": "bytes"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Carrega o contrato para que o Python possa interagir com ele
contrato_biometria = w3.eth.contract(address=contract_address, abi=contract_abi)
print("Conectado à blockchain e contrato carregado.")

# --- 2. DEFINIÇÃO DAS FUNÇÕES DE INTERAÇÃO E MEDIÇÃO ---

def inserir_blockchain(caminho_imagem, biocode):
    """Insere um biocode na blockchain via Smart Contract."""
    biocode_bytes = biocode.tobytes()
    tx_hash = contrato_biometria.functions.guardarBiocode(biocode_bytes).transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)

# Mantenha um contador para saber qual índice ler
blockchain_read_index = 0

def ler_blockchain(caminho_imagem, biocode):
    """Lê um biocode da blockchain pelo seu índice."""
    global blockchain_read_index
    contrato_biometria.functions.lerBiocode(blockchain_read_index).call()
    blockchain_read_index += 1 # Incrementa o índice para a próxima leitura

def medir_desempenho(funcao_alvo, caminho_imagem, biocode):
    """Executa uma função alvo e mede o tempo, CPU e memória gastos."""
    start_time = time.time()
    cpu_antes = psutil.cpu_percent(interval=None)
    mem_antes = psutil.virtual_memory().percent

    funcao_alvo(caminho_imagem, biocode)

    end_time = time.time()
    cpu_depois = psutil.cpu_percent(interval=None)
    mem_depois = psutil.virtual_memory().percent
    tempo_decorrido = end_time - start_time
    
    return {
        "tempo_s": tempo_decorrido,
        "cpu_percent": cpu_depois,
        "mem_percent": mem_depois
    }

# --- 3. LÓGICA PRINCIPAL DE TESTES ---

print("Inserindo um registro inicial na blockchain para aquecimento...")
inserir_blockchain("dummy_path", np.array([0,1,0]))

caminho_datasets = r'C:\Users\Giulia\Documents\TCC2\fvc-going\FVC2004\DB4_B'
seed_usuario = 123

print("\nIniciando testes de desempenho da Blockchain...")

nome_arquivo_csv = 'resultados_blockchain_DB4.csv'
with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
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
                        # Mede inserção na Blockchain
                        resultado_ins = medir_desempenho(inserir_blockchain, caminho_completo, biocode)
                        writer.writerow([caminho_completo, 'insercao', 'Blockchain', resultado_ins['tempo_s'], resultado_ins['cpu_percent'], resultado_ins['mem_percent']])
                        
                        # Mede leitura da Blockchain
                        resultado_read = medir_desempenho(ler_blockchain, caminho_completo, biocode)
                        writer.writerow([caminho_completo, 'leitura_1_1', 'Blockchain', resultado_read['tempo_s'], resultado_read['cpu_percent'], resultado_read['mem_percent']])
                        
                        contador += 1

print(f"\nTestes da Blockchain concluídos! Os resultados de {contador} imagens foram salvos em '{nome_arquivo_csv}'.")