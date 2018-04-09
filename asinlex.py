'''
--------------------------------------------------------------------------------------
======================================================================================

This is the lex file for the Asin programming language

Found below are strings and regular expressions that define each token in Asin

======================================================================================
--------------------------------------------------------------------------------------
'''
import sys
import ply.lex as lex
from asinerrs import *

reserved = {
    # conditional
    'kapag': 'IF',
    'ngunit': 'BUT',
    'kundiman': 'ELSE',
    # loops
    'hanggat': 'WHILE',
    'bawat': 'FOR',
    'sa': 'IN',
    'lumisan': 'EXIT',
    # printing
    'ilimbag': 'PRINT',
    # True or False
    'Totoo': 'TRUE',
    'Huwad': 'FALSE',
    # logical truth value ops
    'at': 'AND',
    'o': 'OR',
    'hindi': 'NOT'
}

tokens = [
    # identifiers, primitives, and newline
    'ID',
    'INTEGER', 'FLOAT', 'STRING',
    'NEWLINE',
    # arithmetic ops
    'PLUS', 'MINUS', 'MUL', 'DIV', 'FDIV', 'EXP', 'MOD',
    # comparison ops
    'EQ', 'NEQ', 'GT', 'GTE', 'LT', 'LTE',
    # grouping symbols
    'LPAREN', 'RPAREN',
    'LSQUARE', 'RSQUARE',
    'LCURLY', 'RCURLY',
    # assignment symbols
    'EQUALS', 'PLUSEQUALS', 'MINUSEQUALS', 'MULEQUALS', 'DIVEQUALS', 'FDIVEQUALS', 'EXPEQUALS', 'MODEQUALS',
    # separators
    'COMMA',
    'COLON', 'SMCOLON'

] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_FDIV = r'//'
t_EXP = r'\*\*'
t_MOD = r'%'
t_EQ = r'=='
t_NEQ = r'!='
t_GT = r'>'
t_GTE = r'>='
t_LT = r'<'
t_LTE = r'<='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_EQUALS = r'='
t_PLUSEQUALS = r'\+='
t_MINUSEQUALS = r'-='
t_MULEQUALS = r'\*='
t_DIVEQUALS = r'/='
t_FDIVEQUALS = r'//='
t_EXPEQUALS = r'\*\*='
t_MODEQUALS = r'%='
t_COMMA = r','
t_COLON = r':'
t_SMCOLON = r';'

t_ignore_WS = r'\s+'
t_ignore_COMMENTS = r'[#].+'


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.linepos = 0
    pass

def t_ID(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_TRUE(t):
    r'Totoo'
    t.value = True
    return t

def t_FALSE(t):
    r'Huwad'
    t.value = False
    return t

def t_FLOAT(t):
    r'\d*\.\d*'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"([\\.]|[^"\\])*"'
    t.value = t.value.lstrip('"')
    t.value = t.value.rstrip('"')
    return t

def t_error(t):
    '''
    Raise a lexical error upon encountering an unrecognized lexeme/token
    '''
    line = open(sys.argv[1]).readlines()[t.lineno - 1]
    raise MaalatNaLeksim(t.lineno, findColumn(sys.argv[1], t), t.value, line)

def findColumn(input,lexeme):
    '''
    Function for computing the position of a lexeme within
    a line of code, as specified in the ply documentation
    '''
    return (lexeme.lexpos - lexeme.lineno) + 1

lexer = lex.lex()