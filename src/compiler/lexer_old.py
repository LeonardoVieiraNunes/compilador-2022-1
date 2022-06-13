#INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

import ply.lex as lex
from compiler.exceptions import InvalidTokenError


class Lexer:
    reserved_keywords = {
        'def': 'DEF',
        'if': 'IF',
        'for': 'FOR',
        'else': 'ELSE',
        'new': 'NEW',
        'int': 'INT_KEYWORD',
        'float': 'FLOAT_KEYWORD',
        'string': 'STRING_KEYWORD',
        'break': 'BREAK',
        'read': 'READ',
        'print': 'PRINT',
        'return': 'RETURN',
    }

    tokens = [
        # Reserved keywords
        *reserved_keywords.values(),

        # Brakets, parentesis and square brackets
        'LBRACKETS',
        'RBRACKETS',
        'LPAREN',
        'RPAREN',
        'LSQBRACKETS',
        'RSQBRACKETS',

        # Boolean operators
        'GREATER_THAN',
        'LOWER_THAN',
        'GREATER_OR_EQUALS_THAN',
        'LOWER_OR_EQUALS_THAN',
        'EQ_COMPARISON',
        'NEQ_COMPARISON',

        # Arithmetic operators
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MODULE',

        # Delimiters
        'SEMICOLON',
        'COMMA',

        # Null
        'NULL',

        # Atribution
        'ATTRIBUTION',

        # Non-trivial tokens
        'IDENT',
        'FLOAT_CONSTANT',
        'INT_CONSTANT',
        'STRING_CONSTANT',
    ]

    # Disclaimer:
    # The PLY package uses the size of the regex expressions to define which
    # will be applyed first, applying the longer first. If the expression is
    # defined using a function, it uses the order which they are defined in
    # source file.
    # Example: if t_INT_CONSTANT comes before t_FLOAT_CONSTANT, it
    # matches all that comes before the dot, and reconize if as integer.
    # Then, it read the dot alone and do not match any expression, and causes
    # an error

    t_LBRACKETS = r'{'
    t_RBRACKETS = r'}'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LSQBRACKETS = r'\['
    t_RSQBRACKETS = r'\]'

    t_GREATER_THAN = r'>'
    t_LOWER_THAN = r'<'
    t_GREATER_OR_EQUALS_THAN = r'>='
    t_LOWER_OR_EQUALS_THAN = r'<='
    t_EQ_COMPARISON = r'=='
    t_NEQ_COMPARISON = r'!='

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'\/'
    t_MODULE = r'%'

    t_SEMICOLON = r';'
    t_COMMA = r','

    t_NULL = r'null'

    t_ATTRIBUTION = r'='

    t_STRING_CONSTANT = r'".*"'

    # Regular expressions with some actions

    def t_IDENT(self, t):
        r'[A-Za-z][A-Za-z0-9_]*'
        # Check identifier word is not a reserved keyword
        t.type = self.reserved_keywords.get(t.value, 'IDENT')
        return t

    def t_FLOAT_CONSTANT(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_INT_CONSTANT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Gets token column
    def find_column(self, token):
        line_start = self._input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    # ERROR
    def t_error(self, t):
        raise InvalidTokenError(
            "ERRO LÉXICO: Caractere inválido '%s' na linha %s, coluna %s" %
            (t.value[0], t.lexer.lineno, self.find_column(t)))

    # Builds lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Lexer input
    def input(self, source_code: str, **kwargs):
        self._input = source_code
        self.lexer.input(source_code, **kwargs)

    # Gets token info
    def token(self):
        return self.lexer.token()
