import ply.lex as lex
import ply.yacc as yacc
from token_generator import *
from print_tables import *
import json
import sys
from prettytable import PrettyTable

def get_tables(lexer):
    types = ['def', 'string', 'int', 'float']

    tokens_table = []
    symbols_table = {}

    tok = ''

    while True:
        last_tok = tok
        tok = lexer.token()

        if not tok:
            break

        tokens_table.append({'token': tok.type, 'valor': tok.value, 'linha': tok.lineno, 'coluna': lexer.find_column(tok)})

        if tok.type == 'IDENT':
            if last_tok.value in types:
                if tok.value in symbols_table:
                    symbols_table[tok.value]['tipo'] = last_tok.value
                    symbols_table[tok.value]['declaracao'] = tok.lineno
                else:
                    symbols_table[tok.value] = {'nome': tok.value, 'tipo': last_tok.value, 'declaracao': tok.lineno, 'referenciacao': []}
            else:
                if tok.value in symbols_table:
                    symbols_table[tok.value]['referenciacao'].append(tok.lineno)
                else:
                    symbols_table[tok.value] = {'nome': tok.value, 'tipo': 'SEM_TIPO','declaracao': 'NAO_DECLARADO', 'referenciacao': [tok.lineno]}

    return tokens_table, symbols_table

def main(data):
    lexer = Lexer()
    lexer.build()
    lexer.input(data)

    tokens_table, symbols_table = get_tables(lexer)

    print_tokens_table(tokens_table)
    print_symbols_table(symbols_table)

input_file = open(sys.argv[1])
data = input_file.read()
input_file.close()
main(data)
