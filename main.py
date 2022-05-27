import sys

from generator import parse
from lex_yacc import ParseException, lex, yacc

if __name__ == "__main__":
    FILENAME = "test.code"

    text = open(FILENAME, "r")
    text = text.read()

    def get_table(text):
        with open("table.txt", "w") as file:
            strings = "".join(text)
            lex.input(strings)
            while 1:
                token = lex.token()
                if not token:
                    break
                file.write(
                    "TOKEN TYPE: %s, VALUE: '%s', LINE: %d\n"
                    % (token.type, token.value, token.lineno)
                )

    get_table(text)

    try:
        ast = yacc.parse(text)
    except ParseException as e:
        print(e)
    else:
        ast_file = open("ast", "w")
        ast_file.write(str(ast))

        asm = open("out.s", "w+")
        # asm.write('# Generated from: ' + sys.argv[1] + '\n')

        parse(ast, asm)
