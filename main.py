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

        a = 0;
        b = 1;
        while (b < 1000) {
            print b;
            b += a;
            a = b - a;
        }

    """

    tokens = lexer.tokenize(text)


    ast = parser.parse(tokens)

    ast.print()

    print('\nChecking syntax...\n')
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    print('\nOkay!\n')

    for error in typeChecker.errors:
        print(f'Error: {error}')
