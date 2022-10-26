import sys
import lexer as lexer


if __name__ == '__main__':

    filename: str = ""
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example_input.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = lexer.SimpleLexer()

    for token in lexer.tokenize(text):
        print(f"({token.lineno}:{token.index}) : {token.type} : '{token.value}'")