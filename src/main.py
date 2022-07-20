#INE5426 - Construção de Compiladores - Analisador Léxico, Sintático, Semântico e GCI
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

import argparse, linecache, sys, json
from compiler.lexer import Lexer
from compiler.exceptions import (InvalidTokenError,
                                 SyntaticError,
                                 BreakWithoutLoopError,
                                 VariableAlreadyDeclaredInScopeError,
                                 InvalidTypeOperationError,
                                 VariableNotDeclared)
from compiler.parser import parser
from compiler.semantic import parse
from compiler.gci import gen_code
from utils.print_tables import get_tables, print_symbols_table, print_tokens_table

def main(filepath):
    with open(filepath) as f:
        source_code = f.read()

    #cria o AL
    lexer = Lexer()
    lexer.build()
    lexer.input(source_code)
    tokens = []

    while True:
        token = lexer.token()
        if not token:
            break
        else:
            tokens.append(token)

    # cria as tabelas de tokens e simbolos
    tokens_table, symbols_table = get_tables(lexer, tokens)

    if lexer.erro > 0:
        print("Análise léxica finalizou com erros")
        print("Abortando o programa...")
        exit(1)

    #print das tabelas
    print_tokens_table(tokens_table)
    print_symbols_table(symbols_table)

    #executa o AS
    print('Executando parser...\n')
    success, fail_token = parser.parse(tokens=tokens)

    if not success:
        line = linecache.getline(filepath, fail_token.lineno)
        print('ERRO SINTÁTICO na linha %s:\n\t%s' %
                    (fail_token.lineno, line.strip()))
        print('Token: %s' % fail_token)

        sys.exit(1)

    else:
        print('Análise sintática completada com sucesso!')

    # executa a Analise Semantica
    try:
        semantic_analyser_result = parse(source_code)

        symbol_tables = semantic_analyser_result['scopes']
        num_expressions = semantic_analyser_result['num_expressions']

        print("As expressões aritméticas são válidas")
        print("As declarações das variáveis por escopo são válidas")
        print("Todo break está no escopo de um for")

    # erro break fora do loop
    except BreakWithoutLoopError as exp:
        lineno = str(exp)
        line = linecache.getline(filepath, int(lineno))
        print("ERRO SEMÂNTICO!")
        print("Uso inválido do break na linha %s:\n\t%s" % (exp, line.strip()))

        sys.exit(1)

    # erro variavel ja declarada no escopo
    except VariableAlreadyDeclaredInScopeError as exp:
        lineno = int(str(exp))
        line = linecache.getline(filepath, lineno)
        print("ERRO SEMÂNTICO!")
        print("Variável já declarada. Primeira declaração na linha %s" % int(str(exp)))
        print(line)
        sys.exit(1)

    # erro operacao invalida entre dois tipos
    except InvalidTypeOperationError as exp:
        left, right, lineno = str(exp).split(',')
        line = linecache.getline(filepath, int(lineno))
        print("ERRO SEMÂNTICO!")
        print("Operação inválida entre %s e %s na linha %s" % (left, right, lineno))
        print(line)
        sys.exit(1)

    # erro varivael nao declarada
    except VariableNotDeclared as exp:
        ident, lineno = str(exp).split(',')
        line = linecache.getline(filepath, int(lineno))
        print("ERRO SEMÂNTICO!")
        print("Variável %s sendo usada antes da declaração na linha %s" % (ident, lineno))
        print(line)
        sys.exit(1)

    print("Análise semântica concluída com sucesso!!")

    # exporta a tabela de simbolos do escopo
    scope_symbol_table_file = 'output/scope_symbol_tables.json'
    print("Tabela de símbolos dos escopos exportada para %s" % scope_symbol_table_file)
    with open(scope_symbol_table_file, 'w') as f:
        json.dump(symbol_tables, f, indent=2, sort_keys=False)

    # exporta a arvore de expressao
    expressions_file = 'output/expressions.json'
    print("Árvore de expressões exportada para %s" % expressions_file)
    with open(expressions_file, 'w') as f:
        json.dump(num_expressions, f, indent=2, sort_keys=False)

    # executa e exporta o GCI
    print("Executando a geração de código intermediário...")
    code = gen_code(source_code)
    gci_file = 'output/gci.txt'
    print("Código intermediário exportado para %s" % gci_file)

    with open(gci_file, 'w') as f:
        f.write(code)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Auxiliar script to execute compiler')
    arg_parser.add_argument('filepath',
                            help='Target source code file')

    args = arg_parser.parse_args()
    main(args.filepath)
