from ply import yacc

from lexer import ParseException

precedence = (
    ("left", "+", "-"),
    ("left", "*", "/"),
)


def p_file(p):
    """file : unit
    | file unit"""
    p[0] = ("unit", p[1], p[2]) if len(p) >= 3 else p[1]


def p_unit(p):
    """unit : fun_def
    | declaration ";" """
    p[0] = p[1]


def p_statement_fun_def(p):
    """fun_def : declaration_specifier ID "(" ")" compound_statement
    | declaration_specifier ID "(" declaration_list ")" compound_statement"""
    if len(p) >= 7:
        p[0] = ("fun", p[1], p[2], p[4], p[6])
    else:
        p[0] = ("fun", p[1], p[2], p[5])


def p_statement_expr(p):
    """statement : expression ";"
    | declaration ";"
    | compound_statement"""
    p[0] = p[1]


def p_statement_fun_call(p):
    """expression : ID "(" ")"
    | ID "(" expression_list ")" """
    p[0] = ("call", p[1], p[3]) if len(p) > 4 else ("call", p[1])


def p_statement_asm_call(p):
    """expression : ASM "(" S_CONST ")" """
    p[0] = (p[1], p[3])


def p_statement_call(p):
    """expression : PRINT "(" S_CONST ")" """
    p[0] = (p[1], p[3])


def p_declaration_specifier(p):
    """declaration_specifier : VOID
    | INT
    | CHAR
    | FLOAT
    """
    p[0] = (p[1], p[2]) if len(p) >= 3 else p[1]


def p_statement_return(p):
    """statement : RETURN expression ";"
    | RETURN ";" """
    p[0] = ("ret", p[2]) if len(p) >= 4 else ("ret",)


def p_statement_break(p):
    """statement : BREAK ";" """
    p[0] = ("break",)


def p_statement_continue(p):
    """statement : CONTINUE ";" """
    p[0] = ("continue",)


def p_statement_while_def(p):
    """statement : WHILE "(" expression ")" statement"""
    p[0] = ("while", p[3], p[5])


def p_statement_if_def(p):
    """statement : IF "(" expression ")" statement"""
    p[0] = ("if", p[3], p[5])


def p_statement_if_else_def(p):
    """statement : IF "(" expression ")" statement ELSE statement"""
    p[0] = ("ifelse", p[3], p[5], p[7])


def p_statement_def(p):
    """declaration : declaration_specifier ID "=" expression
    | declaration_specifier ID"""
    p[0] = ("decli", p[1], p[2], p[4]) if len(p) >= 5 else ("decli", p[1], p[2])


def p_statement_rminusminus(p):
    """expression : MINUSMINUS ID"""
    p[0] = (("assign", p[2], ("binop", "-", ("id", p[2]), "1")), ("id", p[2]))


def p_statement_minusminus(p):
    """expression : ID MINUSMINUS"""
    p[0] = (("id", p[1]), ("assign", p[1], ("binop", "-", ("id", p[1]), "1")))


def p_statement_rplusplus(p):
    """expression : PLUSPLUS ID"""
    p[0] = (("assign", p[2], ("binop", "+", ("id", p[2]), "1")), ("id", p[2]))


def p_statement_plusplus(p):
    """expression : ID PLUSPLUS"""
    p[0] = (("id", p[1]), ("assign", p[1], ("binop", "+", ("id", p[1]), "1")))


def p_statement_xoreq(p):
    """expression : ID XOREQUAL expression"""
    p[0] = ("assign", p[1], ("binop", "^", ("id", p[1]), p[3]))


def p_statement_andeq(p):
    """expression : ID ANDEQUAL expression"""
    p[0] = ("assign", p[1], ("binop", "&", ("id", p[1]), p[3]))


def p_statement_oreq(p):
    """expression : ID OREQUAL expression"""
    p[0] = ("assign", p[1], ("binop", "|", ("id", p[1]), p[3]))


def p_statement_muleq(p):
    """expression : ID TIMESEQUAL expression"""
    p[0] = ("assign", p[1], ("binop", "*", ("id", p[1]), p[3]))


def p_statement_diveq(p):
    """expression : ID DIVEQUAL expression"""
    p[0] = ("assign", p[1], ("binop", "/", ("id", p[1]), p[3]))


def p_statement_pluseq(p):
    """expression : ID PLUSEQUAL expression"""
    p[0] = ("assign", p[1], ("binop", "+", ("id", p[1]), p[3]))


def p_statement_minuseq(p):
    """expression : ID MINUSEQUAL expression"""
    p[0] = ("assign", p[1], ("binop", "-", ("id", p[1]), p[3]))


def p_statement_assign(p):
    """expression : ID "=" expression"""
    p[0] = ("assign", p[1], p[3])


def p_expression_list(p):
    """expression_list : expression
    | expression_list ',' expression"""
    p[0] = (p[1], p[3]) if len(p) >= 3 else p[1]


def p_declaration_list(p):
    """declaration_list : declaration
    | declaration_list ',' declaration"""
    p[0] = (p[1], p[3]) if len(p) >= 3 else p[1]


def p_expression_binop(p):
    """expression : expression '+' expression
    | expression '-' expression
    | expression '*' expression
    | expression '/' expression
    """
    p[0] = ("binop", p[2], p[1], p[3])


def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = ("uminus", p[2])


def p_expression_group(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]


def p_expression_number(p):
    """expression : NUMBER
    | FLOAT"""
    p[0] = p[1]


def p_expression_name(p):
    """expression : ID"""
    p[0] = ("id", p[1])


def p_expression_char(p):
    """expression : C_CONST"""
    p[0] = ("char", p[1])


def p_cond_exp(p):
    """expression : eq_exp"""
    p[0] = p[1]


def p_eq_exp(p):
    """eq_exp : expression EQ expression
    | expression NE expression
    | expression LOR expression
    | expression LAND expression
    | expression '<' expression
    | expression '>' expression
    | expression GE expression
    | expression LE expression"""
    p[0] = ("cond", p[2], p[1], p[3])


def p_compound_statement(p):
    """compound_statement : "{" statement_list "}"
    | "{" "}" """
    if len(p) >= 4:
        p[0] = p[2]


def p_statement_list(p):
    """statement_list : statement
    | statement_list statement"""
    p[0] = (p[1], p[2]) if len(p) >= 3 else p[1]


def p_error(p):
    if p:
        raise ParseException(f"Syntax error at: {p.value} line: {str(p.lineno)}")
    else:
        raise ParseException("Syntax error at EOF")


yacc.yacc()
