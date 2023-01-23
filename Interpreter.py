import AST
import SymbolTable
from Memory import MemoryStack
from Exceptions import *
from VisitDecorators import when, on
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory = MemoryStack()

    @on("node")
    def visit(self, node):
        pass

    @when(AST.StatementList)
    def visit(self, node: AST.StatementList):
        for statement in node.statements:
            self.visit(statement)

    @when(AST.PrintStatement)
    def visit(self, node: AST.PrintStatement):
        evaluated_expression = self.visit(node.expression)
        print(evaluated_expression)

    @when(AST.AssignmentStatement)
    def visit(self, node: AST.AssignmentStatement):
        self.memory.set_variable(node.identifier.name, self.visit(node.expression))

    @when(AST.WhileStatement)
    def visit(self, node: AST.WhileStatement):
        while self.visit(node.expression):
            self.visit(node.statement)

    @when(AST.BinaryOperation)
    def visit(self, node: AST.BinaryOperation):
        left = self.visit(node.left_expression)
        right = self.visit(node.right_expression)

        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            return left / right
        elif node.operator == '.+':
            pass
            # TODO
        elif node.operator == '.-':
            pass
            # TODO
        elif node.operator == '.*':
            pass
            # TODO
        elif node.operator == './':
            pass
            # TODO
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == '>=':
            return left >= right
        elif node.operator == '<=':
            return left <= right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>':
            return left > right
        

    @when(AST.Primitive)
    def visit(self, node: AST.Primitive):
        return node.value.value if isinstance(node.value, AST.Number) else node.value

    @when(AST.LValue)
    def visit(self, node: AST.LValue):
        return self.memory.get_variable(node.name)

    #  @when(AST.BinOp)
    # def visit(self, node):
    #     r1 = node.left.accept(self)
    #     r2 = node.right.accept(self)
    # try sth smarter than:
    # if(node.op=='+') return r1+r2
    # elsif(node.op=='-') ...
    # but do not use python eval

    # @when(AST.Assignment)
    # def visit(self, node):
    # #
    # #

    # # simplistic while loop interpretation
    # @when(AST.WhileInstr)
    # def visit(self, node):
    #     r = None
    #     while node.cond.accept(self):
    #         r = node.body.accept(self)
    #     return r
