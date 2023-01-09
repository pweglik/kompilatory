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

    b = "abc";

    a = 3;
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
