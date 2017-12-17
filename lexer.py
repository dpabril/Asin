import ply.lex as lex

reserved = {
	'if': 'IF',
	'elsif': 'ELSIF',
	'else': 'ELSE',

	'for': 'FOR',
	'while': 'WHILE',

	'fxn': 'FUNCTION',
	'return': 'RETURN',

	'print': 'SAY',

	'and': 'AND',
	'or': 'OR',
	'not': 'NOT',
}