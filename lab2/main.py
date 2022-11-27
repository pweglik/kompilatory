from parser import SimpleParser
from lexer import SimpleLexer

def draw_ast(node):
    if node[0] == "Statement":
        print("\n\n")
        print(node)
        
    if node[0] == "Program" or node[0] == "StatementList":
        for el in node[1:]:
            if el is not None:
                draw_ast(el)
        

if __name__ == '__main__':
    lexer = SimpleLexer()
    parser = SimpleParser()

    text = '''
    for i = 1:N
    for j = 1:M
    print i,j;

    '''

    tokens = lexer.tokenize(text)
    for t in lexer.tokenize(text):
        print(t)
    result = parser.parse(tokens)
    # print(f'\n{result}')
    draw_ast(result)



    # while True:
    #     try:
    #         text = input("$ ")
    #         result = parser.parse(lexer.tokenize(text))
    #         print(result)
    #     except EOFError:
    #         break