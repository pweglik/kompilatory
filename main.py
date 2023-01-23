#!/usr/bin/env python3

from Interpreter import Interpreter
from TypeChecker import TypeChecker
from SimpleParser import SimpleParser
from SimpleLexer import SimpleLexer


if __name__ == "__main__":
    lexer = SimpleLexer()
    parser = SimpleParser()

    text = \
    """
    n = 10;
    for i = 1:n print "*" * i;

    # a = 0;
    # b = 1;
    # while (b < 1000) {
    #     print b;
    #     b = a + b;
    #     a = b - a;
    # }

    """

    tokens = lexer.tokenize(text)

    ast = parser.parse(tokens)

    ast.print()

    print("\nChecking syntax...\n")
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    print("\nFinished type checking!\n")

    for error in typeChecker.errors:
        print(f'Error: {error}')

    print('\nInterpreting...\n')
    interpreter = Interpreter()
    interpreter.visit(ast)
