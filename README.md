# Armazenamento Seguro de Dados Biométricos 

> Uma análise comparativa de métodos e tecnologias para a garantia de integridade e segurança em dados sensíveis.

## Sobre o Projeto

Este projeto foi desenvolvido como requisito para obtenção do grau de Bacharel em Sistemas de Informação pela Universidade do Estado do Amazonas (UEA).

O objetivo principal foi investigar e comparar diferentes arquiteturas para o armazenamento de dados biométricos, focando em **Segurança**, **Integridade** e **Desempenho**. Diante da sensibilidade dos dados pessoais (LGPD), a pesquisa analisou como tecnologias tradicionais se comparam a abordagens descentralizadas.

### Cenário Analisado
A comparação foi realizada entre três abordagens distintas:
1.  **Relacional (SQL):** Utilizando **PostgreSQL**.
2.  **Não-Relacional (NoSQL):** Utilizando **MongoDB**.
3.  **Descentralizada (Blockchain):** Utilizando conceitos de **Blockchain Privada** para imutabilidade.

## Tecnologias Utilizadas

* **Linguagem:** Python
* **Bancos de Dados:** PostgreSQL, MongoDB
* **Algoritmos de Segurança:** Hashing (SHA-256)
* **Conceitos:** Blockchain, Imutabilidade, Integridade de Dados, LGPD.

## Metodologia e Resultados

Foram desenvolvidos scripts em Python para simular a inserção e leitura de grandes volumes de dados biométricos (hash/templates) em cada uma das tecnologias.

**Principais conclusões da análise:**
* **Integridade:** A implementação em Blockchain demonstrou superioridade na garantia da imutabilidade do registro, sendo ideal para auditoria.
* **Desempenho (Inserção):** O **MongoDB** apresentou a melhor performance para inserção em lote.
* **Desempenho (Leitura):** O **PostgreSQL** apresentou a melhor performance para leitura em lote.
* **Segurança:** A análise comparativa destacou os trade-offs entre a rapidez dos bancos tradicionais e a segurança criptográfica da blockchain.

## Estrutura do Repositório

```bash
├── analise/          # Dados consolidados e utilizados na análise e gráficos gerados
├── docs/             # Documentação completa (TCC em PDF)
├── fvc-going/        # Dataset FVC (Fingerprint Verification Competition)
├── scripts/          # Scripts de automação, testes de inserção e leitura nas 3 tecnologias análisadas. 
├── resultados/       # Dados obtidos da execução dos testes
└── README.md         # Resumo do projeto
