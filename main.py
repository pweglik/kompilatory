from my_parser import SimpleParser
from lexer import SimpleLexer
from draw_ast import draw_ast
import pydot

if __name__ == '__main__':
    lexer = SimpleLexer()
    parser = SimpleParser()

    text='''
# A-=10;
# A = 10;
# A = A-1;
# A = -A-1;

# N = 10;
# M = 20;

for i = 1:2 {
    c = 10;
}


# for i = 1:N {
    # for j = i:M {
    #     # print i, j;
    #     C = 10;
    # }
# }

# while(k>0) {
#     if(k<5)
#         i = 1;
#     else if(k<10)
#         i = 2;   
#     else
#         i = 3;
    
#     k = k - 1;
# }



    '''
    
    tokens = lexer.tokenize(text)

    # for t in lexer.tokenize(text):
    #     print(t)

    result = parser.parse(tokens)

    # for statement in result:
    #     print(statement)

    # draw_ast(result)
    # print(result)
    result.print()
    dot = pydot.Dot(graph_type='digraph')
    node = result.graph(dot)

    # dot.write_pdf('ast.pdf')
    # dot.write_png('ast.png')
