#INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

import argparse, linecache, sys
from compiler.lexer import Lexer
from compiler.exceptions import (InvalidTokenError,
                                 SyntaticError,
                                 )
from compiler.parser import parser

def main(filepath):
    with open(filepath) as f:
        source_code = f.read()

    tokens = []
    lexer = Lexer()
    lexer.build()
    lexer.input(source_code)
    while True:
        token = lexer.token()
        if not token:
            break
        else:
            tokens.append(token)

    if Lexer.erro > 0:
        print("Análise léxica finalizou com erros")
        print("Abortando o programa...")
        exit(1)
    
    print('Número de tokens: %s' % len(tokens))

    print('\nExecutando parser...')
    success, fail_token = parser.parse(tokens=tokens)

    if not success:
        line = linecache.getline(filepath, fail_token.lineno)
        print('ERRO SINTÁTICO na linha %s:\n\t%s' %
                    (fail_token.lineno, line.strip()))
        print('Token: %s' % fail_token)

        sys.exit(1)

    else:
        print('Análise sintática completada com sucesso!')

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Auxiliar script to execute compiler')
    arg_parser.add_argument('filepath',
                            help='Target source code file')

    args = arg_parser.parse_args()
    main(args.filepath)