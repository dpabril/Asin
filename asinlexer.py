import ply.lex as lex

reserved = {
    'kapag': 'IF',
    'kundi': 'ELSE',

    'hanggat': 'WHILE',
    #'lumisan': 'EXIT',

    'itakda': 'FUNCTION',
    'isauli': 'RETURN',

    'ilimbag': 'PRINT',

    'at': 'AND',
    'o': 'OR',
    'hindi': 'NOT',
}

tokens = [
    'ID',
    'INTEGER',
    'FLOAT',
    'STRING',
    'NEWLINE',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'LCURLY',
    'RCURLY',
    'COMMA',
    'EQUALS',
    'COLON',
    'SMCOLON',

    'PLUS',
    'MINUS',
    'MUL',
    'DIV',
    'MOD',

    'TRUE',
    'FALSE',

    'EQ',
    'NEQ',
    'GT',
    'GTE',
    'LT',
    'LTE',

] + list(reserved.values())

t_COMMA = r','
t_PLUS = r'\+'
t_MINUS = '-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_SMCOLON = r';'
t_EQUALS = r'='
t_ignore_WS = r'\s+'
t_COLON = ':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\{'
t_RBRACK = r'\}'
t_LSQBRACK = r'\['
t_RSQBRACK = r'\]'
t_EQ = r'=='
t_NEQ = r'!='
t_GT = r'>'
t_GTE = r'>='
t_LT = r'<'
t_LTE = r'<='
t_ignore_COMMENTS = r'//.+'


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.linepos = 0
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, t.type)\
    return t


def t_FLOAT(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"(?:\\"|.)*?"'
    t.value = bytes(t.value.lstrip('"').rstrip('"'), "utf-8").decode("unicode_escape")
    return t

def t_TRUE(t):
    'Totoo'
    t.value = True
    return t


def t_FALSE(t):
    'Huwad'
    t.value = False
    return t


# def t_error(t):
    # raise mamba.exceptions.UnexpectedCharacter("Unexpected character '%s' at line %d" % (t.value[0], t.lineno))


lexer = lex.lex()