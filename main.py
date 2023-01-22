#!/usr/bin/env python3

from TypeChecker import TypeChecker
from my_parser import SimpleParser
from lexer import SimpleLexer
from draw_ast import draw_ast
import pydot

if __name__ == "__main__":
    lexer = SimpleLexer()
    parser = SimpleParser()

    text = \
    """

    A = zeros(1);
    A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere

E1 = [ [ 1, 2, 3],
       [ 4, 5, 6],
       [ 7, 8, 9] ];


# A[1,3] = 0 ;


    """

    tokens = lexer.tokenize(text)


    ast = parser.parse(tokens)

    ast.print()
    dot = pydot.Dot(graph_type="digraph")
    node = ast.graph(dot)

    typeChecker = TypeChecker()
    typeChecker.visit(ast)

    for error in typeChecker.errors:
        print(f'Error: {error}')

    # dot.write_pdf('ast.pdf')
    dot.write_png("ast.png")
