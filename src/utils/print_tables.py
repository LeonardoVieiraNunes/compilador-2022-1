#INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

from prettytable import PrettyTable

def print_tokens_table(tokens_table):
    """Print da tabela de tokens"""
    print("========= TABELA DE TOKENS =========")
    t = PrettyTable(['TOKEN', 'VALOR', 'LINHA', 'COLUNA'])
    for tt in tokens_table:
        t.add_row([tt['token'], tt['valor'],tt['linha'], tt['coluna']])
    print(t)
    print()

def print_symbols_table(symbols_table):
    """Print da tabela de simbolos"""
    print("========= TABELA DE SÍMBOLOS =========")
    t = PrettyTable(['NOME', 'TIPO', 'DECLARAÇÃO (linha)', 'REFERENCIADO (linha)'])
    for key in symbols_table:
        ss = symbols_table[key]
        t.add_row([ss['nome'], ss['tipo'],ss['declaracao'], ss['referenciacao']])
    print(t)
    print()

def get_tables(lexer, tokens):
    """Obtem tabelas de tokens e simbolos"""
    #lista com os tipos dos identificadores
    types = ['def', 'string', 'int', 'float']

    # tabela de tokens e de simbolos
    tokens_table = []
    symbols_table = {}

    tok = ''

    for i in range(len(tokens)):
        #pega as info do token atual
        last_tok = tok

        tok = tokens[i]

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
