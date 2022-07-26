#INE5426 - Construção de Compiladores - Analisador Léxico e Sintático
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

class InvalidTokenError(Exception):
    """Lexical analyser fails to parse source code"""


class SyntaticError(Exception):
    """Invalid production to be applied on parsing"""


class BreakWithoutLoopError(Exception):
    """Semantic error when a break is written without a loop scope"""


class InvalidTypeOperationError(Exception):
    """Semantic error when two variables are invalid operated"""


class VariableAlreadyDeclaredInScopeError(Exception):
    """Semantic error when a variable is declared twice inside the same scope"""


class VariableNotDeclared(Exception):
    """Semantic error when a variable was used before declared"""
