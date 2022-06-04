# INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

import ply.lex as lex
import ply.yacc as yacc
from token_generator import *
import sys

tokens = Lexer.tokens

# Regras da gramática

# Epsilon
def p_empty(p):
    '''
    empty :
    '''
    pass

def p_program_statement(p):
    '''
    PROGRAM : STATEMENT
                | FUNCLIST
                | empty
    '''
    pass

def p_funclist(p):
    '''
    FUNCLIST : FUNCDEF FUNCLIST2
    '''
    pass

def p_funclist2(p):
    '''
    FUNCLIST2 : FUNCLIST 
                | empty
    '''
    pass

def p_funcdef(p):
	'''
	FUNCDEF : DEF IDENT '(' PARAMLIST ')'  '{' STATELIST '}'
	'''
	pass

def p_paramlist(p):
    '''
    PARAMLIST : INT PARAMLIST2 
                | FLOAT PARAMLIST2 
                | STRING PARAMLIST2 
                | empty
    '''
    pass

# PARAMLIST' (linha) no relatório
def p_paramlist2(p):
    '''
    PARAMLIST2 : IDENT PARAMLIST3
    '''
    pass

# PARAMLIST2 no relatorio
def p_paramlist3(p):
    '''
    PARAMLIST3 : ',' PARAMLIST
                | empty
    '''
    pass

def p_statement(p):
    '''
    STATEMENT : VARDECL ';' 
                | ATRIBSTAT ';' 
                | PRINTSTAT ';' 
                | READSTAT ';' 
                | RETURNSTAT ';'
                | IFSTAT ';'
                | FORSTAT ';'
                | '{' STATELIST '}'
                | BREAK ';'
                | ';'
    '''
    pass

def p_vardecl(p):
    '''
    VARDECL : INT VARDECL2 
            | FLOAT VARDECL2 
            | STRING VARDECL2
    '''
    pass

def p_vardecl2(p):
    '''
    VARDECL2 : IDENT VARDECL3
    '''
    pass

def p_vardecl3(p):
    '''
    VARDECL3 : '[' INTCONSTANT ']' VARDECL3
            | empty
    '''
    pass

def p_atribstat(p):
    '''
    ATRIBSTAT : LVALUE '=' RIGHTATRIBSTAT
    '''
    pass

def p_rightatribstat(p):
    '''
    RIGHTATRIBSTAT : EXPRESSION 
                    | ALLOCEXPRESSION 
                    | FUNCCALL
    '''
    pass

def p_funccall(p):
    '''
    FUNCCALL : IDENT '(' PARAMLISTCALL ')'
    '''
    pass

def p_paramlistcall(p):
    '''
    PARAMLISTCALL : IDENT PARAMLISTCALL2 
                    | empty
    '''
    pass

def p_paramlistcall2(p):
    '''
    PARAMLISTCALL2 : ',' PARAMLISTCALL 
                    | empty
    '''
    pass

def p_printstat(p):
    '''
    PRINTSTAT : PRINT EXPRESSION
    '''
    pass

def p_readstat(p):
    '''
    READSTAT : READ LVALUE
    '''
    pass

def p_returnstat(p):
    '''
    RETURNSTAT : RETURN
    '''
    pass

def p_ifstat(p):
    '''
    IFSTAT : IF '(' EXPRESSION ')' STATEMENT ELSESTAT
    '''
    pass

def p_elsestat(p):
    '''
    ELSESTAT : ELSE STATEMENT 
                | empty
    '''
    pass

def p_forstat(p):
    '''
    FORSTAT : FOR '(' ATRIBSTAT ';' EXPRESSION ';' ATRIBSTAT ')' STATEMENT
    '''
    pass

def p_statelist(p):
    '''
    STATELIST : STATEMENT STATELIST2
    '''
    pass


def p_statelist2(p):
    '''
    STATELIST2 : STATELIST 
                | empty
    '''
    pass

# 2 é '
def p_allocexpression(p):
    '''
    ALLOCEXPRESSION : NEW ALLOCEXPRESSION2
    '''
    pass

def p_allocexpression2(p):
    '''
    ALLOCEXPRESSION2 : INT ALLOCEXPRESSION_OPT 
                    | FLOAT ALLOCEXPRESSION_OPT 
                    | STRING ALLOCEXPRESSION_OPT
    '''
    pass

# 3 é 2
def p_allocexpression_opt(p):
    '''
    ALLOCEXPRESSION_OPT : '[' NUMEXPRESSION ']' ALLOCEXPRESSION3
    '''
    pass

def p_allocexpression3(p):
    '''
    ALLOCEXPRESSION3 : ALLOCEXPRESSION_OPT 
                        | empty
    '''
    pass

def p_expression(p):
    '''
    EXPRESSION : NUMEXPRESSION EXPRESSION2
    '''
    pass

def p_expression2(p):
    '''
    EXPRESSION2 : '<' NUMEXPRESSION 
                | '>' NUMEXPRESSION 
                | LTE NUMEXPRESSION 
                | GTE NUMEXPRESSION 
                | EQUAL NUMEXPRESSION 
                | INEQUAL NUMEXPRESSION
    '''
    pass

def p_numexpression(p):
    '''
    NUMEXPRESSION : TERM NUMEXPRESSION2
    '''
    pass

def p_numexpression2(p):
    '''
    NUMEXPRESSION2 : '+' TERM NUMEXPRESSION 
                    | '-' TERM NUMEXPRESSION 
                    | empty
    '''
    pass

def p_term(p):
    '''
    TERM : UNARYEXPR UNARYEXPR2
    '''
    pass

def p_unaryexpression2(p):
    '''
    UNARYEXPR2 : '*' UNARYEXPR2 
                | '/' UNARYEXPR2 
                | '%' UNARYEXPR2 
                | empty
    '''
    pass

def p_unaryexpression(p):
    '''
    UNARYEXPR : '+' FACTOR 
                | '-' FACTOR 
                | FACTOR
    '''
    pass

def p_factor(p):
    '''
    FACTOR : INTCONSTANT 
            | FLOATCONSTANT 
            | STRINGCONSTANT 
            | NULL 
            | LVALUE 
            | '(' NUMEXPRESSION ')'
    '''
    pass

def p_lvalue(p):
    '''
    LVALUE : IDENT LVALUE2
    '''
    pass

def p_lvalue2(p):
    '''
    LVALUE2 : '[' NUMEXPRESSION ']' LVALUE2 
            | empty
    '''
    pass

# Erro
def p_error(p):
    if p:
        print(f"ERRO SINTÁTICO: linha {p.lineno}, token \'{p.value}\'")
    else:
        print('ERRO SINTATICO em EOF')
    pass


# Le arquivo
input_file = open(sys.argv[1])
data = input_file.read()
input_file.close()

# Lexer
lexer = Lexer()
lexer.build()
lexer.input(data)

# Parser
parser = yacc.yacc(start='PROGRAM')
result = parser.parse(data)
print(result)