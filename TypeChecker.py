#!/usr/bin/env python3

import AST
from SymbolTable import *


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable(None, 'main')
        self.loopcount = 0

    def visit_StatementList(self, node):
        
        for statement in node.statements:
            self.visit(statement)



    def visit_WhileStatement(self, node):
        self.loopcount += 1

        # self.symbol_table = self.symbol_table.pushScope("While")
        self.visit(node.expression)
        self.visit(node.statement)

        self.loopcount -= 1
        # self.symbol_table = self.symbol_table.popScope()

    def visit_JumpStatement(self, node):
        if node.name == "BREAK" or node.name == "CONTINUE":
            if self.loopcount == 0:
                print("Break/Continue outside of loop: ", node.line_number)

        else: # RETURN
            self.visit(node.expression)