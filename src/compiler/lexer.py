#INE5426 - Construção de Compiladores - Analisador Léxico e Sintático
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

import ply.lex as lex
import ply.yacc as yacc
from compiler.exceptions import InvalidTokenError


class Lexer(object):
    erro = 0
    # tokens list
    tokens = ['PLUS',
              'MINUS',
              'TIMES',
              'DIVIDE',
              'MOD',
              'ASSIGN',
              'LT',
              'GT',
              'LTE',
              'GTE',
              'EQUAL',
              'INEQUAL',
              'DOT',
              'COMMA',
              'SEMICOLON',
              'RIGHTPARENTHESES',
              'LEFTPARENTHESES',
              'RIGHTBRACKET',
              'LEFTBRACKET',
              'RIGHTBRACE',
              'LEFTBRACE',
              'DIGITO',
              'LETRA',
              'INTCONSTANT',
              'STRINGCONSTANT',
              'FLOATCONSTANT',
              'IDENT'
              ]

    #regular expression
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'
    t_ASSIGN = r'='
    t_LT = r'<'
    t_GT = r'>'
    t_LTE = r'<='
    t_GTE = r'>='
    t_EQUAL = r'=='
    t_INEQUAL = r'!='
    t_DOT = r'\.'
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_RIGHTPARENTHESES = r'\)'
    t_LEFTPARENTHESES = r'\('
    t_RIGHTBRACKET = r'\]'
    t_LEFTBRACKET = r'\['
    t_RIGHTBRACE = r'}'
    t_LEFTBRACE = r'{'
    t_DIGITO = r'([0-9])'
    t_LETRA = r'([A-Za-z])'

    # Ignores spaces
    t_ignore = ' \t'


    #reserved words
    reserved = {
                'int': 'INT',
                'float': 'FLOAT',
                'string': 'STRING',
                'new': 'NEW',
                'def': 'DEF',
                'break': 'BREAK',
                'print': 'PRINT',
                'return': 'RETURN',
                'read': 'READ',
                'if': 'IF',
                'else': 'ELSE',
                'for': 'FOR',
                'null': 'NULL',
                }

    tokens = tokens + list(reserved.values())

    # LINEBREAK
    def t_LINEBREAK(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        pass

    # FLOATCONSTANT
    def t_FLOATCONSTANT(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    # INTCONSTANT
    def t_INTCONSTANT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # STRING
    def t_STRINGCONSTANT(self, t):
        r'"[^\n"\r]*"'
        return t

    # IDENT
    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'IDENT')
        return t

    # ERROR
    def t_error(self, t):
        column = self.find_column(t)
        print("-----------------------------------------")
        print("ERRO LÉXICO")
        print("Caracter: '%s'" % t.value[0])
        print("Linha: %s" % t.lexer.lineno)
        print("Coluna: %s" % column)
        print("-----------------------------------------")
        Lexer.erro += 1
        t.lexer.skip(1)

    # pega a coluna do token
    def find_column(self, token):
        input = self.lexer.lexdata
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    #constroi o AL
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    #passa uma entrada pro AL
    def input(self, code: str, **kwargs):
        self._input = code
        self.lexer.input(code, **kwargs)

    #pega as info do token
    def token(self):
        return self.lexer.token()

    #funcao para testes dos tokens
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)
