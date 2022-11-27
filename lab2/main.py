from Parser import SimpleParser
from lexer import SimpleLexer


if __name__ == '__main__':
    lexer = SimpleLexer()
    parser = SimpleParser()

    text = '''5;'''

    tokens = lexer.tokenize(text)
    for t in lexer.tokenize(text):
        print(t)
    result = parser.parse(tokens)
    print(result)



    # while True:
    #     try:
    #         text = input("$ ")
    #         result = parser.parse(lexer.tokenize(text))
    #         print(result)
    #     except EOFError:
    #         break