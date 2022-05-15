#INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

import ply.lex as lex
import ply.yacc as yacc
from token_generator import *
from print_tables import *
import json
import sys
from prettytable import PrettyTable

def get_tables(lexer):
    #lista com os tipos dos identificadores
    types = ['def', 'string', 'int', 'float']

    # tabela de tokens e de simbolos
    tokens_table = []
    symbols_table = {}

    tok = ''

    while True:
        #pega as info do token atual
        last_tok = tok
        tok = lexer.token()

        if not tok:
            break

        #adiciona o token atual na tabela de tokens
        tokens_table.append({'token': tok.type, 'valor': tok.value, 'linha': tok.lineno, 'coluna': lexer.find_column(tok)})

        #verifica se é identificador
        if tok.type == 'IDENT':
            if last_tok.value in types:
                #verifica se ja foi referenciado antes
                if tok.value in symbols_table:
                    symbols_table[tok.value]['tipo'] = last_tok.value
                    symbols_table[tok.value]['declaracao'] = tok.lineno
                #se nao foi referenciado ainda:
                else:
                    symbols_table[tok.value] = {'nome': tok.value, 'tipo': last_tok.value, 'declaracao': tok.lineno, 'referenciacao': []}
            #apenas referenciacao
            else:
                #ja foi declarado antes
                if tok.value in symbols_table:
                    symbols_table[tok.value]['referenciacao'].append(tok.lineno)
                else:
                    symbols_table[tok.value] = {'nome': tok.value, 'tipo': 'SEM_TIPO','declaracao': 'NAO_DECLARADO', 'referenciacao': [tok.lineno]}

    return tokens_table, symbols_table

def main(data):
    #cria o AL
    lexer = Lexer()
    lexer.build()
    lexer.input(data)

    #cria as tabelas de tokens e simbolos
    tokens_table, symbols_table = get_tables(lexer)

    #print das tabelas
    print_tokens_table(tokens_table)
    print_symbols_table(symbols_table)

#passa um arquivo de entrada pra main()
input_file = open(sys.argv[1])
data = input_file.read()
input_file.close()
main(data)
