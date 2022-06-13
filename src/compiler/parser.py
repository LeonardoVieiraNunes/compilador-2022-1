#INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

import os
from typing import List, Tuple, Optional
from collections import deque

from ply.lex import LexToken

from utils.cfg_processor import CfgProcessor
from utils.data_structures import SyntaticAnalyserMatrix, SymbolTableType
from compiler.exceptions import SyntaticError


TYPE_TO_TERMINAL_MAP = {
    'DEF': 'def',
    'IF': 'if',
    'FOR': 'for',
    'ELSE': 'else',
    'NEW': 'new',
    'INT': 'int',
    'FLOAT': 'float',
    'STRING': 'string',
    'BREAK': 'break',
    'READ': 'read',
    'PRINT': 'print',
    'RETURN': 'return',
    'LEFTBRACE': '{',
    'RIGHTBRACE': '}',
    'LEFTPARENTHESES': '(',
    'RIGHTPARENTHESES': ')',
    'LEFTBRACKET': '[',
    'RIGHTBRACKET': ']',
    'GT': '>',
    'LT': '<',
    'GTE': '>=',
    'LTE': '<=',
    'EQUAL': '==',
    'INEQUAL': '!=',
    'PLUS': '+',
    'MINUS': '-',
    'TIMES': '*',
    'DIVIDE': '/',
    'MOD': '%',
    'SEMICOLON': ';',
    'COMMA': ',',
    'NULL': 'null',
    'ASSIGN': '=',
    'IDENT': 'ident',
    'FLOATCONSTANT': 'float_constant',
    'INTCONSTANT': 'int_constant',
    'STRINGCONSTANT': 'string_constant',
    'STACK_BOT': '$'
}

STACK_BOT_TOKEN = LexToken()
STACK_BOT_TOKEN.type = 'STACK_BOT'


class Parser:
    def __init__(self):
        curr_file_folder = os.path.dirname(__file__)
        grammar_path = os.path.join(curr_file_folder,
                                    'ConvCC-2022-1.csf')

        cfg_proc = CfgProcessor()
        cfg_proc.read(grammar_path)

        self.cfg = cfg_proc.cfg
        self.start_symbol = cfg_proc.cfg.start_symbol
        self.mat = cfg_proc.generate_matrix()

        self.__empty_symbol = '&'

    def parse(self, tokens: List[LexToken]) -> Tuple[bool, Optional[LexToken]]:
        """Validate symbols and update symbols_table"""
        stack = deque()

        stack.append('$')
        stack.append(self.start_symbol)

        for token in tokens + [STACK_BOT_TOKEN]:
            token_terminal = TYPE_TO_TERMINAL_MAP[token.type]
            while True:
                # Terminal on top of stack and on code pointer
                # are equals, pop the stack and move the pointer
                if token_terminal == stack[-1]:
                    stack.pop()
                    break

                # Get production to be applied
                try:
                    prod = self.mat.get_prod(stack[-1], token_terminal)
                except KeyError:
                    return (False, token)

                # Reconize syntatic error
                if prod is None:
                    return (False, token)

                # Remove the top of the stack
                stack.pop()

                # Stack the symbols from corresponding production
                for symbol in reversed(prod.body):
                    if symbol != self.__empty_symbol:
                        stack.append(symbol)

        # If something other than the stack bottom is in the stack
        if len(stack) > 1:
            return (False, token)

        return (True, None)


parser = Parser()
