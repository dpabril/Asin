import ply.lex as lex

reserved = {
    'kapag':'IF',
    'kundi':'ELSE',

    'hanggat':'WHILE',
    'lumisan':'BREAK',

    'itakda':'FUNCTION',
    'isauli':'RETURN',

    'ilimbag':'PRINT',

    'at':'AND',
    'o':'OR',
    'hindi':'NOT'
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
    'RSQAURE',
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
    'LTE'
] + list(reserved.values())