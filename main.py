#!/usr/bin/env python3

from TypeChecker import TypeChecker
from SimpleParser import SimpleParser
from SimpleLexer import SimpleLexer


if __name__ == "__main__":
    lexer = SimpleLexer()
    parser = SimpleParser()

    text = """    
x = zeros(4);
x[0][1] = 2;

# x = ones(3,5)
# z = x[7,10]
# v = x[2,3,4]


"""

    tokens = lexer.tokenize(text)

    ast = parser.parse(tokens)

    ast.print()

    print("\nChecking syntax...\n")
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    print("\nFinished type checking!\n")

    for error in typeChecker.errors:
        print(f"Error: {error}")
