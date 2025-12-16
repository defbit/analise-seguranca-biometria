import cv2
import numpy as np

def extrair_vetor_da_imagem(caminho_imagem):
    """
    Lê uma imagem de impressão digital, a converte para escala de cinza
    e a transforma em um vetor unidimensional (array 1D).
    """
    # O segundo parâmetro '0' garante que a imagem seja lida em escala de cinza
    img = cv2.imread(caminho_imagem, 0)
    
    # Verifica se a imagem foi carregada corretamente
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem em {caminho_imagem}")
        return None
    
    # Transforma a matriz 2D da imagem em um vetor 1D
    vetor_plano = img.flatten()
    
    return vetor_plano

def gerar_biocode(vetor_caracteristicas, seed_usuario, tamanho_biocode=1024):
    """
    Aplica o algoritmo BioHashing a um vetor de características para gerar um BioCode binário.
    """
    if vetor_caracteristicas is None:
        return None

    # define a semente para o gerador de números aleatórios do NumPy.
    # garante que a 'chave' seja sempre a mesma para a mesma seed.
    np.random.seed(seed_usuario)

    # gera uma matriz de projeção com números aleatórios.
    # as dimensões são [tamanho do vetor original] x [tamanho do BioCode desejado].
    matriz_aleatoria = np.random.randn(len(vetor_caracteristicas), tamanho_biocode)

    # realiza a projeção do vetor de características na matriz aleatória (produto escalar).
    vetor_projetado = np.dot(vetor_caracteristicas, matriz_aleatoria)

    # binariza o resultado: se o valor for > 0, se torna 1; senão, se torna 0.
    biocode = (vetor_projetado > 0).astype(int)
    
    return biocode

# Bloco de teste: executar apenas quando este script é rodado diretamente
if __name__ == "__main__":
    # Caminho genérico para exibição no documento
    caminho_exemplo = r'dataset/FVC2004/DB1_B/101_1.tif' 

    print(f"Processando a imagem: {caminho_exemplo}")
    
    # Passo 1: Extrair o vetor da imagem
    vetor = extrair_vetor_da_imagem(caminho_exemplo)
    
    if vetor is not None:
        print(f"Vetor extraído com sucesso. Tamanho: {len(vetor)}")
        
        # Passo 2: Gerar o BioCode usando uma 'seed' de exemplo
        seed_exemplo = 123
        biocode_gerado = gerar_biocode(vetor, seed_exemplo)
        
        if biocode_gerado is not None:
            print(f"BioCode gerado com sucesso. Tamanho: {len(biocode_gerado)}")
            print("Amostra do BioCode (primeiros 30 dígitos):")
            print(biocode_gerado[:30])
