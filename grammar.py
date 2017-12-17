'''
    statement_list : statement
                   | statement_list statement

	statement : assign_statement
              | if_statement
              | while_statement
              | func_decl_statement
              | function_call_statement
              | return_statement
              | print_statement

	assign_statement : identifier EQUALS assignable SMCOLON
              |

	if_statement : IF condition LCURLY statement_list RCURLY
				 | IF condition LCURLY statement_list RCURLY ELSE LCURLY statement_list RCURLY
				 | IF condition LCURLY statement_list RCURLY ELSE if_statement

	while_statement : WHILE condition LCURLY statement_list RCURLY

	func_decl_statement : FUNCTION identifier LPAREN arguments RPAREN LCURLY statement_list RCURLY
              			| FUNCTION identifier LCURLY statement_list RCURLY

  function_call_statement : function_call SMCOLON

	return_statement : RETURN expression SMCOLON

	print_statement : PRINT arguments SMCOLON

	function_call : identifier LPAREN arguments RPAREN

	identifier : ID

	primitive : INT_NUM
              | FLOAT_NUM
              | STRING
              | boolean

  boolean : TRUE
    		  | FALSE

	condition : expression EQ expression
            | expression NEQ expression
            | expression GT expression
            | expression GTE expression
            | expression LT expression
            | expression LTE expression
            | expression AND expression
            | expression OR expression
	
	expression : expression PLUS expression %prec PLUS
            | expression MINUS expression %prec MINUS
            | expression MUL expression %prec MUL
            | expression DIV expression %prec DIV
            | expression MOD expression %prec MOD

	expression : MINUS expression %prec UMINUS
               | NOT expression

	expression : LPAREN expression RPAREN

	expression : LSQUARE arguments RSQUARE

	expression : identifier LSQUARE expression COLON expression RSQUARE
               | identifier LSQUARE COLON expression RSQUARE
               | identifier LSQUARE expression COLON RSQUARE
               | identifier LSQUARE COLON RSQUARE
    # ^ Array slicing

	expression : primitive
               | identifier
               | function_call

	assignable : primitive
               | expression

	arguments : arguments COMMA expression
              | expression
              |
'''