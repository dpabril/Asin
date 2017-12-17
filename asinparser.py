import ply.yacc as yacc
from asinlexer import tokens

disable_warnings = False

precedence = (
    ('left', 'NOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('left', 'EXP', 'MOD'),
    ('right', 'UMINUS'),
)

def p_statement_list(p):
    '''
    statement_list : statement
                   | statement_list statement
    '''

def p_statement(p):
    '''
    statement : assign_statement
              | if_statement
              | while_statement
              | function_decl_statement
              | function_call_statement
              | return_statement
              | print_statement
    '''

def p_assign_statement(p):
    '''
    assign_statement : identifier EQUALS assignable SMCOLON
    '''

def p_if_statement(p):
    '''
    if_statement : IF condition LCURLY statement_list RCURLY
                 | IF condition LCURLY statement_list RCURLY ELSE LCURLY statement_list RCURLY
                 | IF condition LCURLY statement_list RCURLY ELSE if_statement
    '''

def p_while_statement(p):
    '''
    while_statement : WHILE condition LCURLY statement_list RCURLY
    '''

def p_function_decl_statement(p):
    '''
    function_decl_statement : FUNCTION identifier LPAREN arguments RPAREN LCURLY statement_list RCURLY
                        | FUNCTION identifier LCURLY statement_list RCURLY
    '''

def p_function_call_statement(p):
    '''
    function_call_statement : function_call SMCOLON
    '''

def p_return_statement(p):
    '''
    return_statement : RETURN expression SMCOLON
    '''

def p_print_statement(p):
    '''
    print_statement : PRINT arguments SMCOLON
    '''

def p_function_call(p):
    '''
    function_call : identifier LPAREN arguments RPAREN
    '''

def p_identifier(p):
    '''
    identifier : ID
    '''

def p_primitive(p):
    '''
    primitive : INT_NUM
              | FLOAT_NUM
              | STRING
              | boolean
    '''

def p_boolean(p):
    '''
    boolean : TRUE
            | FALSE
    '''

def p_condition(p):
    '''
    condition : expression EQ expression
            | expression NEQ expression
            | expression GT expression
            | expression GTE expression
            | expression LT expression
            | expression LTE expression
            | expression AND expression
            | expression OR expression
    '''

def p_expression_BinOp(p):
    '''
    expression : expression PLUS expression
            | expression MINUS expression
            | expression MUL expression
            | expression DIV expression
            | expression MOD expression
    '''

def p_expression_UnaOp(p):
    '''
    expression : MINUS expression %prec UMINUS
               | NOT expression
    '''

def p_expression_Paren(p):
    '''
    expression : LPAREN expression RPAREN
    '''

def p_exprsesion_Square(p):
    '''
    expression : LSQUARE arguments RSQUARE
    '''

def p_expression_ArrSlice(p):
    '''
    expression : identifier LSQUARE expression COLON expression RSQUARE
               | identifier LSQUARE COLON expression RSQUARE
               | identifier LSQUARE expression COLON RSQUARE
               | identifier LSQUARE COLON RSQUARE
    '''

def p_expression_Single(p):
    '''
    expression : primitive
               | identifier
               | function_call
    '''

def p_assignable(p):
    '''
    assignable : primitive
               | expression
    '''

def p_arguments(p):
    '''
    arguments : arguments COMMA expression
              | expression
              |
    '''