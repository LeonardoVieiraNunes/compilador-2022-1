import ply.lex as lex
import ply.yacc as yacc
from token_generator import *

# def main(data):
lexer = Lexer()
lexer.build()
lexer.test("3 + 4")
