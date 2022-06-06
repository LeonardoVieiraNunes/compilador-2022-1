# INE5426 - Construção de Compiladores - Analisador Léxico
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

import ply.lex as lex
import ply.yacc as yacc
from token_generator import *
import sys
import logging

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
    p[0] = p[1]

def p_funclist(p):
    '''
    FUNCLIST : FUNCDEF FUNCLIST2
    '''
    if p[2]==None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_funclist2(p):
    '''
    FUNCLIST2 : FUNCLIST 
                | empty
    '''
    p[0] = p[1]

def p_funcdef(p):
    '''
    FUNCDEF : DEF IDENT LEFTPARENTHESES PARAMLIST RIGHTPARENTHESES  LEFTBRACE STATELIST RIGHTBRACE
	'''
    if p[4]==None:
        statelist = ''.join(p[7])
        p[0] = p[1]+p[2]+p[3]+p[5]+p[6]+statelist+p[8]
    else:
        p[0] = ' '.join(p[1:])

def p_paramlist(p):
    '''
    PARAMLIST : INT PARAMLIST2 
                | FLOAT PARAMLIST2 
                | STRING PARAMLIST2 
                | empty
    '''
    if p[1]==None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

# PARAMLIST' (linha) no relatório
def p_paramlist2(p):
    '''
    PARAMLIST2 : IDENT PARAMLIST3
    '''
    if p[2]==None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

# PARAMLIST2 no relatorio
def p_paramlist3(p):
    '''
    PARAMLIST3 : COMMA PARAMLIST
                | empty
    '''
    if p[1]==None:
        p[0]=p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_statement(p):
    '''
    STATEMENT : VARDECL SEMICOLON 
                | ATRIBSTAT SEMICOLON 
                | PRINTSTAT SEMICOLON 
                | READSTAT SEMICOLON 
                | RETURNSTAT SEMICOLON
                | IFSTAT SEMICOLON
                | FORSTAT SEMICOLON
                | LEFTBRACE STATELIST RIGHTBRACE
                | BREAK SEMICOLON
                | SEMICOLON
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_vardecl(p):
    '''
    VARDECL : INT VARDECL2 
            | FLOAT VARDECL2 
            | STRING VARDECL2
    '''
    p[0] = ' '.join(p[1:])

def p_vardecl2(p):
    '''
    VARDECL2 : IDENT VARDECL3
    '''
    if p[2] == None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_vardecl3(p):
    '''
    VARDECL3 : LEFTBRACKET INTCONSTANT RIGHTBRACKET VARDECL3
            | empty
    '''
    if p[1] == None:
        p[0] = p[1]
    elif p[4] == None:
        p[0] = p[1] + str(p[2]) + p[3]
    else:
        prox_vardecl3 = ''.join(p[4])
        p[0] = p[1] + str(p[2]) + p[3] + prox_vardecl3

def p_atribstat(p):
    '''
    ATRIBSTAT : LVALUE ASSIGN RIGHTATRIBSTAT
    '''
    p[0] = ' '.join(p[1:])

def p_rightatribstat(p):
    '''
    RIGHTATRIBSTAT : EXPRESSION 
                    | ALLOCEXPRESSION 
                    | FUNCCALL
    '''
    p[0] = p[1]

def p_funccall(p):
    '''
    FUNCCALL : IDENT LEFTPARENTHESES PARAMLISTCALL RIGHTPARENTHESES
    '''
    if p[3]==None:
        p[0] = p[1]+p[2]+p[4]
    else:
        p[0] = ' '.join(p[1:])

def p_paramlistcall(p):
    '''
    PARAMLISTCALL : IDENT PARAMLISTCALL2 
                    | empty
    '''
    if p[1]==None or p[2]==None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_paramlistcall2(p):
    '''
    PARAMLISTCALL2 : COMMA PARAMLISTCALL 
                    | empty
    '''
    if p[1]==None or p[2]==None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_printstat(p):
    '''
    PRINTSTAT : PRINT EXPRESSION
    '''
    p[0] = ' '.join(p[1:])

def p_readstat(p):
    '''
    READSTAT : READ LVALUE
    '''
    p[0] = ' '.join(p[1:])

def p_returnstat(p):
    '''
    RETURNSTAT : RETURN
    '''
    p[0] = p[1]

def p_ifstat(p):
    '''
    IFSTAT : IF LEFTPARENTHESES EXPRESSION RIGHTPARENTHESES STATEMENT ELSESTAT
    '''
    if p[6]==None:
        p[0] = ' '.join(p[1:6])
    else:
        p[0] = ' '.join(p[1:])

def p_elsestat(p):
    '''
    ELSESTAT : ELSE STATEMENT 
                | empty
    '''
    if p[1]==None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_forstat(p):
    '''
    FORSTAT : FOR LEFTPARENTHESES ATRIBSTAT SEMICOLON EXPRESSION SEMICOLON ATRIBSTAT RIGHTPARENTHESES STATEMENT
    '''
    p[0] = ' '.join(p[1:])

def p_statelist(p):
    '''
    STATELIST : STATEMENT STATELIST2
    '''
    if p[2]==None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])


def p_statelist2(p):
    '''
    STATELIST2 : STATELIST 
                | empty
    '''
    p[0] = p[1]

# 2 é '
def p_allocexpression(p):
    '''
    ALLOCEXPRESSION : NEW ALLOCEXPRESSION2
    '''
    p[0] = ' '.join(p[1:])

def p_allocexpression2(p):
    '''
    ALLOCEXPRESSION2 : INT ALLOCEXPRESSION_OPT 
                    | FLOAT ALLOCEXPRESSION_OPT 
                    | STRING ALLOCEXPRESSION_OPT
    '''
    p[0] = ' '.join(p[1:])

# 3 é 2
def p_allocexpression_opt(p):
    '''
    ALLOCEXPRESSION_OPT : LEFTBRACKET NUMEXPRESSION RIGHTBRACKET ALLOCEXPRESSION3
    '''
    if p[4]==None:
        p[0] = ' '.join(p[1:4])
    else:
        p[0] = ' '.join(p[1:])

def p_allocexpression3(p):
    '''
    ALLOCEXPRESSION3 : ALLOCEXPRESSION_OPT 
                        | empty
    '''
    p[0] = p[1]

def p_expression(p):
    '''
    EXPRESSION : NUMEXPRESSION EXPRESSION2
    '''
    p[0] = ' '.join(p[1:])

def p_expression2(p):
    '''
    EXPRESSION2 : LT NUMEXPRESSION 
                | GT NUMEXPRESSION 
                | LTE NUMEXPRESSION 
                | GTE NUMEXPRESSION 
                | EQUAL NUMEXPRESSION 
                | INEQUAL NUMEXPRESSION
    '''
    p[0] = ' '.join(p[1:])

def p_numexpression(p):
    '''
    NUMEXPRESSION : TERM NUMEXPRESSION2
    '''
    if p[2]==None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_numexpression2(p):
    '''
    NUMEXPRESSION2 : PLUS TERM NUMEXPRESSION 
                    | MINUS TERM NUMEXPRESSION 
                    | empty
    '''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_term(p):
    '''
    TERM : UNARYEXPR UNARYEXPR2
    '''
    if p[2]==None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_unaryexpression2(p):
    '''
    UNARYEXPR2 : TIMES UNARYEXPR2
                | DIVIDE UNARYEXPR2
                | MOD UNARYEXPR2
                | empty
    '''
    if p[1]==None:
        p[0] = p[1]
    else:
        if p[2]==None:
            p[0] = p[1]
        else:
            p[0] = ' '.join(p[1:])

def p_unaryexpression(p):
    '''
    UNARYEXPR : PLUS FACTOR
                | MINUS FACTOR
                | FACTOR
    '''
    p[0] = ' '.join(p[1:])

def p_factor(p):
    '''
    FACTOR : INTCONSTANT
            | FLOATCONSTANT
            | STRINGCONSTANT
            | NULL
            | LVALUE
            | LEFTPARENTHESES NUMEXPRESSION RIGHTPARENTHESES
    '''
    if len(p)==2:
        p[0] = str(p[1])
    else:
        p[0] = ' '.join(p[1:])

def p_lvalue(p):
    '''
    LVALUE : IDENT LVALUE2
    '''
    if p[2]==None:
        p[0] = p[1]
    else:
        p[0] = ' '.join(p[1:])

def p_lvalue2(p):
    '''
    LVALUE2 : LEFTBRACKET NUMEXPRESSION RIGHTBRACKET LVALUE2
            | empty
    '''
    if p[1]==None:
        p[0] = p[1]
    else:
        if p[4]==None:
            p[0] = ' '.join(p[1:4])
        else:
            p[0] = ' '.join(p[1:])

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

# Set up a logging object
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# Lexer
lexer = Lexer()
lexer.build()
lexer.input(data)

# Parser
parser = yacc.yacc(start='PROGRAM')
result = parser.parse(data, debug=logging.getLogger())
print(result)