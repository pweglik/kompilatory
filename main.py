#!/usr/bin/env python3

from my_parser import SimpleParser
from lexer import SimpleLexer
from draw_ast import draw_ast
import pydot

if __name__ == "__main__":
    lexer = SimpleLexer()
    parser = SimpleParser()

    text = """
    # control flow instruction

for a = 1:3
{
    a = 5;
}

# # N = 10;
# # M = 20;
# # for i = 1:N {
# #     for j = i:M {
# #         print i, j;
# #     }
# # }

# if (k < 5)
# {
#     i = 1;
# } else {
#     a = 3;
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


# D1 = A.+B' ; # add element-wise A with transpose of B
# D2 -= A.-B' ; # substract element-wise A with transpose of B
# D3 *= A.*B' ; # multiply element-wise A with transpose of B
# D4 /= A./B' ; # divide element-wise A with transpose of B

    # C = zeros(4);
    # B = ones(4);
    # A = eye(4);
    """

    tokens = lexer.tokenize(text)

    # for t in lexer.tokenize(text):
    #     print(t)

    result = parser.parse(tokens)

    # for statement in result:
    #     print(statement)

    # draw_ast(result)
    # print(result)
    result.print()
    dot = pydot.Dot(graph_type="digraph")
    node = result.graph(dot)

    # dot.write_pdf('ast.pdf')
    dot.write_png("ast.png")
