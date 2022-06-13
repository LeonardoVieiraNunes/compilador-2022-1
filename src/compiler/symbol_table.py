#INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

from typing import List, Union
from dataclasses import dataclass
from ply.lex import LexToken
from utils.data_structures import SymbolRow, SymbolTableType


SYMBOLS_TO_TABLE = ['IDENT']


def generate_symbol_table(tokens: List[LexToken],
                          default_type: str = 'Unknow') -> SymbolTableType:
    """Generate symbol table using SYMBOLS_TO_TABLE as orientation"""
    symbols_table: SymbolTableType = {}
    for i, token in enumerate(tokens):
        if token.type in SYMBOLS_TO_TABLE:
            if token.value in symbols_table:
                symbols_table[token.value].lines_referenced.append(
                    token.lineno)

            else:
                symbols_table[token.value] = SymbolRow(
                    var_name=token.value,
                    token_index=i,
                    type=default_type,
                    line_declared=token.lineno,
                    lines_referenced=[]
                )

    return symbols_table
