import ply.lex as lex


class ParseException(Exception):
    pass


# Reserved words
reserved = (
    "BREAK",
    "CHAR",
    "CONTINUE",
    "ELSE",
    "FOR",
    "IF",
    "INT",
    "FLOAT",
    "RETURN",
    "WHILE",
    "PRINT",
)

tokens = reserved + (
    "ID",
    "NUMBER",
    # Logical operatores (||, &&, <=, >=, ==, !=)
    "LOR",
    "LAND",
    "LE",
    "GE",
    "EQ",
    "NE",
    # Assignment (*=, /=, +=, -=, &=, ^=, |=)
    "TIMESEQUAL",
    "DIVEQUAL",
    "PLUSEQUAL",
    "MINUSEQUAL",
    "ANDEQUAL",
    "XOREQUAL",
    "OREQUAL",
)

literals = [
    "=",
    "+",
    "-",
    "*",
    "/",
    "&&",
    "||",
    "(",
    ")",
    "{",
    "}",
    ";",
    ",",
    "!",
    "<",
    ">",
]

# Tokens

# Operators
t_LOR = r"\|\|"
t_LAND = r"&&"
t_LE = r"<="
t_GE = r">="
t_EQ = r"=="
t_NE = r"!="

# Assignment operators

t_TIMESEQUAL = r"\*="
t_DIVEQUAL = r"/="
t_PLUSEQUAL = r"\+="
t_MINUSEQUAL = r"-="


reserved_map = {r.lower(): r for r in reserved}


def t_ID(t):
    r"""[A-Za-z_][\w_]*"""
    t.type = reserved_map.get(t.value, "ID")
    return t


def t_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")


def t_comment(t):
    r"""/\*(.|\n)*?\*/"""
    t.lexer.lineno += t.value.count("\n")


def t_comment2(t):
    r"""\/\/([^\\\n])*?\n"""
    t.lexer.lineno += t.value.count("\n")


def t_preprocessor(t):
    r"""\#(.)*?\n"""
    t.lexer.lineno += 1


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lex.lex()
