from parser import SimpleParser
from lexer import SimpleLexer
from draw_ast import draw_ast

if __name__ == '__main__':
    lexer = SimpleLexer()
    parser = SimpleParser()

    text='''
    # control flow instruction

N = 10;
M = 20;
for i = 1:N {
    for j = i:M {
        print i, j;
    }
}

while(k>0) {
    if(k<5)
        i = 1;
    else if(k<10)
        i = 2;   
    else
        i = 3;
    
    k = k - 1;
}

a[1][2] = b;


    '''
    
    tokens = lexer.tokenize(text)

    # for t in lexer.tokenize(text):
    #     print(t)

    result = parser.parse(tokens)

    # for statement in result:
    #     print(statement)

    draw_ast(result)
