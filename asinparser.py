import ply.yacc as yacc
from asinlexer import *

disable_warnings = False

precedence = (
    ('left', 'NOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('left', 'EXP', 'MOD'),
    ('right', 'UMINUS'),
)

def p_statement_block(p):
    '''
    statement_block : statement
                   | statement_block statement
    '''
    if len(p) == 2:
        p[0] = asinast.CodeBlock([p[1]])
    else:
        p[1].children.append(p[2])
        p[0] = p[1]
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
    p[0] = p[1]

def p_assign_statement(p):
    '''
    assign_statement : identifier EQUALS assignable SMCOLON
                     | identifier LSQUARE expression RSQUARE EQUALS expression SMCOLON
    '''
    if len(p) == 5:
        p[0] = asinast.AssignStmt(p[1], p[3])
    else if len(p) == 7:
        p[0] = asinast.ArrAssign(p[1], p[3], p[6])

def p_if_statement(p):
    '''
    if_statement : IF condition LCURLY statement_block RCURLY
                 | IF condition LCURLY statement_block RCURLY ELSE LCURLY statement_block RCURLY
                 | IF condition LCURLY statement_block RCURLY ELSE if_statement
    '''
    plen = len(p)
    if plen == 6:
        p[0] = asinast.IfStmt(p[2], p[4])
    else if plen == 10:
        p[0] = asinast.IfStmt(p[2], p[4], p[8])
    else if plen = 8:
        p[0] = asinast.IfStmt(p[2], p[4], p[7])

def p_while_statement(p):
    '''
    while_statement : WHILE condition LCURLY statement_block RCURLY
    '''
    p[0] = ast.WhileStmt(p[2], p[4])

def p_function_decl_statement(p):
    '''
    function_decl_statement : FUNCTION identifier LPAREN arguments RPAREN LCURLY statement_block RCURLY
                            | FUNCTION identifier LCURLY statement_block RCURLY
    '''
    p[2].isfunc = True

    plen = len(p)
    if plen == 9:
        p[0] = asinast.Assignment(p[2], asinast.Function(p[4], p[7]))
    else if plen == 6:
        p[0] = asinast.Assignment(p[2], asinast.Function(asinast.CodeBlock(), p[4]))

def p_function_call_statement(p):
    '''
    function_call_statement : function_call SMCOLON
    '''
    p[0] = p[1]

def p_function_call(p):
    '''
    function_call : identifier LPAREN arguments RPAREN
    '''
    p[1].isfunc = True
    p[0] = asinast.FunctionCall(p[1], p[3])

def p_return_statement(p):
    '''
    return_statement : RETURN expression SMCOLON
    '''
    p[0] = asinast.ReturnStmt(p[2])

def p_print_statement(p):
    '''
    print_statement : PRINT arguments SMCOLON
    '''
    p[0] = asinast.PrintStmt(p[2])


def p_identifier(p):
    '''
    identifier : ID
    '''
    p[0] = asinast.Identifier(p[1])

def p_primitive(p):
    '''
    primitive : INT_NUM
              | FLOAT_NUM
              | STRING
              | TRUE
              | FALSE
    '''
    if isinstance(p[1], asinast.Molecule):
        p[0] = p[1]
    else:
        p[0] = asinast.Primitive(p[1])

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
    p[0] = asinast.BinOp(p[1], p[2], p[3])

def p_expression_BinOp(p):
    '''
    expression : expression PLUS expression
            | expression MINUS expression
            | expression MUL expression
            | expression DIV expression
            | expression MOD expression
    '''
    p[0] = asinast.BinOp(p[1], p[2], p[3])

def p_expression_UnaOp(p):
    '''
    expression : MINUS expression %prec UMINUS
               | NOT expression
    '''
    p[0] = asinast.UnaOp(p[1], p[2])

def p_expression_Paren(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    if isinstance(p[2], asinast.Molecule):
        p[0] = p[2]
    else:
        asinast.Primitive(p[2])

def p_expression_Arr(p):
    '''
    expression : LSQUARE arguments RSQUARE
    '''
    p[0] = asinast.Array(p[2])

def p_expression_ArrAccess(p):
    '''
    expression : identifier LSQUARE expression RSQUARE
    '''
    p[0] = asinast.ArrAccess(p[1], p[3])

def p_expression_ArrSlice(p):
    '''
    expression : identifier LSQUARE expression COLON expression RSQUARE
               | identifier LSQUARE COLON expression RSQUARE
               | identifier LSQUARE expression COLON RSQUARE
               | identifier LSQUARE COLON RSQUARE
    '''
    plen = len(p)
    if plen == 7:
        p[0] = asinast.ArrSlice(p[1], p[3], p[5])
    elif plen == 5:
        p[0] = asinast.ArrSlice(p[1])
    elif p[3] == ':':
        p[0] = asinast.ArrSlice(p[1], end=p[4])
    else:
        p[0] = asinast.ArrSlice(p[1], start=p[3])

def p_expression_Single(p):
    '''
    expression : primitive
               | identifier
               | condition
               | function_call
    '''
    p[0] = p[1]

def p_assignable(p):
    '''
    assignable : primitive
               | expression
    '''
    p[0] = p[1]

def p_arguments(p):
    '''
    arguments : arguments COMMA expression
              | expression
              |
    '''
    plen = len(p)
    if plen == 2:
        p[0] = asinast.CodeBlock([p[1]])
    elif plen == 1:
        p[0] = asinast.CodeBlock()
    else:
        p[1].children.append(p[3])
        p[0] = p[1]