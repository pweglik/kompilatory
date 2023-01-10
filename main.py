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
    """break;

    """

    tokens = lexer.tokenize(text)


    ast = parser.parse(tokens)

    ast.print()
    dot = pydot.Dot(graph_type="digraph")
    node = ast.graph(dot)

    typeChecker = TypeChecker()
    typeChecker.visit(ast)

    # dot.write_pdf('ast.pdf')
    dot.write_png("ast.png")
