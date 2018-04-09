'''
--------------------------------------------------------------------------------------
======================================================================================

This is the yacc file for the Asin programming language. It contains Asin's grammar in
Backus-Naur Form as compliant with yacc.

======================================================================================
--------------------------------------------------------------------------------------
'''
import sys
import ply.yacc as yacc
from asinlex import *
from asinnodes import *
from asinerrs import *

# Setting the precedence rules of operators
precedence = (
    ('left', 'NOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'FDIV'),
    ('left', 'EXP', 'MOD'),
    ('right', 'UMINUS'),
)

def p_stmtBlock(p):
    '''
    statementblock : statementblock statement
                   | statement
    '''
    if len(p) == 2:
        # if statement is singular
        p[0] = SaltBlock([p[1]])
    else:
        # if there are multiple statements; repeatedly append statement (p[2]) to parent SaltBlock
        p[1].grains.append(p[2])
        p[0] = p[1]

def p_stmt(p):
    '''
    statement : assign_statement
              | comp_assign_statement
              | if_statement
              | loop_statement
              | print_statement
              | function_call_statement
              | exit_statement
    '''
    p[0] = p[1]

def p_assignStmt(p):
    '''
    assign_statement : identifier EQUALS expression SMCOLON
    '''
    # if assigning a value to a variable
    p[0] = AssignStmt(p[1], p[3])

def p_compAssignStmt(p):
    '''
    comp_assign_statement : identifier PLUSEQUALS expression SMCOLON
                          | identifier MINUSEQUALS expression SMCOLON
                          | identifier MULEQUALS expression SMCOLON
                          | identifier DIVEQUALS expression SMCOLON
                          | identifier FDIVEQUALS expression SMCOLON
                          | identifier EXPEQUALS expression SMCOLON
                          | identifier MODEQUALS expression SMCOLON
    '''
    p[0] = CompAssignStmt(p[1], p[2], p[3])

def p_ifStmt(p):
    '''
    if_statement : IF LPAREN expression RPAREN LCURLY statementblock RCURLY
                 | IF LPAREN expression RPAREN LCURLY statementblock RCURLY ELSE LCURLY statementblock RCURLY
                 | IF LPAREN expression RPAREN LCURLY statementblock RCURLY BUT if_statement
    '''
    plen = len(p)
    if plen == 8:
        # Rule 1:
        # if only an if clause is recognized
        p[0] = IfStmt(p[3], p[6])
    elif plen == 12:
        # Rule 2:
        # if an if clause and an else-if clause are recognized
        # allows an else clause to still exist since statementblock (p[8]) can be another if_statement
        p[0] = IfStmt(p[3], p[6], p[10])
    elif plen == 10:
        # Rule 3:
        # if only an if clause and else clause is recognized
        p[0] = IfStmt(p[3], p[6], p[9])

def p_loopStmt(p):
    '''
    loop_statement : while_statement
                   | for_statement
    '''
    p[0] = p[1]

def p_whileStmt(p):
    '''
    while_statement : WHILE LPAREN expression RPAREN LCURLY statementblock RCURLY
    '''
    p[0] = WhileStmt(p[3], p[6])

def p_forStmt(p):
    '''
    for_statement : IN FOR identifier IN LSQUARE expression COLON expression RSQUARE LCURLY statementblock RCURLY
    '''
    p[0] = ForStmt(p[3], p[6], p[8], p[11])

def p_printStmt(p):
    '''
    print_statement : PRINT LPAREN commasepexpr RPAREN SMCOLON
    '''
    p[0] = PrintStmt(p[3])

def p_functionCallStatement(p):
    '''
    function_call_statement : function_call SMCOLON
    '''
    p[0] = p[1]

def p_functionCall(p):
    '''
    function_call : identifier LPAREN commasepexpr RPAREN
                  | identifier LPAREN RPAREN
    '''
    # isfunc tells the program that the identifier (p[1]) refers to the name of a function, so the program would act accordingly
    p[1].isfunc = True
    plen = len(p)
    if plen == 5:
        p[0] = AsinFunctionCall(p[1], p[3])
    elif plen == 4:
        p[0] = AsinFunctionCall(p[1])

def p_exitStmt(p):
    '''
    exit_statement : EXIT SMCOLON
    '''
    p[0] = ExitStmt()

def p_identifier(p):
    '''
    identifier : ID
    '''
    p[0] = Identifier(p[1])

def p_primitive(p):
    '''
    primitive : INTEGER
              | FLOAT
              | STRING
              | TRUE
              | FALSE
    '''
    p[0] = Primitive(p[1])

def p_exprCondition(p):
    '''
    expression : expression EQ expression
               | expression NEQ expression
               | expression GT expression
               | expression GTE expression
               | expression LT expression
               | expression LTE expression
               | expression AND expression
               | expression OR expression
    '''
    p[0] = BinOp(p[1], p[2], p[3])

def p_exprBinMathOp(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression MUL expression
               | expression DIV expression
               | expression FDIV expression
               | expression EXP expression
               | expression MOD expression
    '''
    p[0] = BinOp(p[1], p[2], p[3])

def p_exprUnaOp(p):
    '''
    expression : MINUS expression %prec UMINUS
               | NOT expression
    '''
    p[0] = UnaOp(p[1], p[2])

def p_exprGroup(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    if isinstance(p[2], Grain):
        # if expression (p[2]) is expandable
        p[0] = p[2]
    else:
        # if expression (p[2]) is a primitive
        Primitive(p[2])

def p_exprArr(p):
    '''
    expression : LSQUARE commasepexpr RSQUARE
               | LSQUARE RSQUARE
    '''
    plen = len(p)
    if plen == 3:
        p[0] = Array()
    elif plen == 4:
        p[0] = Array(p[2])

def p_exprArrAccess(p):
    '''
    expression : identifier LSQUARE expression RSQUARE
    '''
    p[0] = ArrAccess(p[1], p[3])

def p_exprAtom(p):
    '''
    expression : primitive
               | identifier
               | function_call
    '''
    p[0] = p[1]

def p_commasepexpr(p):
    '''
    commasepexpr : commasepexpr COMMA expression
                 | expression
                 |
    '''
    plen = len(p)
    if plen == 1:
        # if there are no arguments
        p[0] = SaltBlock()
        # pass
    if plen == 2:
        # if the argument is singular
        p[0] = SaltBlock([p[1]])
    else:
        # if there is more than 1 argument, repeatedly append expression (p[3]) to parent node SaltBlock
        p[1].grains.append(p[3])
        p[0] = p[1]

def p_error(p):
    '''
    This defines the errors that yacc will raise upon encountering faulty syntax
    '''
    line = open(sys.argv[1]).readlines()[p.lineno - 1]
    if p is not None:
        raise MaalatNaPalaugnayan(p.lineno, findColumn(sys.argv[1], p), p.value, line)
    else:
        raise MaalatNaPalaugnayan()

def buildParser():
    '''
    Builds the parser through yacc.yacc() and returns it
    '''
    return yacc.yacc(errorlog=yacc.NullLogger())