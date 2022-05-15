#INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

from prettytable import PrettyTable

#print da tabela de tokens
def print_tokens_table(tokens_table):
    print("========= TABELA DE TOKENS =========")
    t = PrettyTable(['TOKEN', 'VALOR', 'LINHA', 'COLUNA'])
    for tt in tokens_table:
        t.add_row([tt['token'], tt['valor'],tt['linha'], tt['coluna']])
    print(t)
    print()

#print da tabela de simbolos
def print_symbols_table(symbols_table):
    print("========= TABELA DE SÍMBOLOS =========")
    t = PrettyTable(['NOME', 'TIPO', 'DECLARAÇÃO (linha)', 'REFERENCIADO (linha)'])
    for key in symbols_table:
        ss = symbols_table[key]
        t.add_row([ss['nome'], ss['tipo'],ss['declaracao'], ss['referenciacao']])
    print(t)
    print()
