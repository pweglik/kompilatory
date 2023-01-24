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

    for i = [1,3,5,7] print "*" * i;

    A = [1,2,3,4,5];
    b = A[0];

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
