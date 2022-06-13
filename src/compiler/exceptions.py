#INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

class InvalidTokenError(Exception):
    """Lexical analyser fails to parse source code"""


class SyntaticError(Exception):
    """Invalid production to be applied on parsing"""
