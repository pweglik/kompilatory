from parser import SimpleParser
from lexer import SimpleLexer
from draw_ast import draw_ast

if __name__ == '__main__':
    lexer = SimpleLexer()
    parser = SimpleParser()

    text='''
    
    B = A[1][2][3];

    '''
    
    tokens = lexer.tokenize(text)

    # for t in lexer.tokenize(text):
    #     print(t)

    result = parser.parse(tokens)

    # for statement in result:
    #     print(statement)

    draw_ast(result)
