#INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

from prettytable import PrettyTable

def print_tokens_table(tokens_table):
    print("========= TABELA DE TOKENS =========")
    t = PrettyTable(['TOKEN', 'VALOR', 'LINHA', 'COLUNA'])
    for entrie in tokens_table:
        t.add_row([entrie['token'], entrie['valor'],entrie['linha'], entrie['coluna']])
    print(t)
    print()


# def print_token_list(tokens_list):
#     print("========= Tokens List =========")
#     for tok in tokens_list:
#         print(tok)
#     print()
#

def print_symbols_table(symbols_table):
    print("========= TABELA DE SÍMBOLOS =========")
    t = PrettyTable(['NOME', 'TIPO', 'DECLARAÇÃO (linha)', 'REFERENCIADO (linha)'])
    for key in symbols_table:
        symbol = symbols_table[key]
        t.add_row([symbol['nome'], symbol['tipo'],symbol['declaracao'], symbol['referenciacao']])
    print(t)
    print()
