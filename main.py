#!/usr/bin/env python3

from TypeChecker import TypeChecker
from SimpleParser import SimpleParser
from SimpleLexer import SimpleLexer

if __name__ == "__main__":
    lexer = SimpleLexer()
    parser = SimpleParser()

    text = \
    """
#     C = [1, 2, 3];
#     A = zeros(1);
#     A = zeros(5);  # create 5x5 matrix filled with zeros
# B = ones(7);   # create 7x7 matrix filled with ones
# I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere

# E1 = [ [ 1, 2, 3],
#          [ 4, 5, 6],
#        [ 7, 8, 9] ];

A = 2 + 3;
# B = [1, 2];
# C = [1, 2, 3];
# D = B + C;


# A[1][3] = 0;


    """

    tokens = lexer.tokenize(text)


    ast = parser.parse(tokens)

    ast.print()

    print('\nChecking syntax...\n')
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    print('\nFinished type checking!\n')

    for error in typeChecker.errors:
        print(f'Error: {error}')
