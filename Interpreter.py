import AST
import SymbolTable
from Memory import MemoryStack
from Exceptions import *
from VisitDecorators import when, on
import sys
import numpy as np

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
        
        right = self.visit(node.expression)

        if node.ass_operator == "=":
            self.memory.set_variable(node.identifier.name, right)
        else:
            variable = self.memory.get_variable(node.identifier.name)
            if node.ass_operator == "+=":
                self.memory.set_variable(node.identifier.name, variable + right)
            elif node.ass_operator == "-=":
                self.memory.set_variable(node.identifier.name, variable - right)
            elif node.ass_operator == "*=":
                self.memory.set_variable(node.identifier.name, variable * right)
            elif node.ass_operator == "/=":
                self.memory.set_variable(node.identifier.name, variable / right)

    @when(AST.WhileStatement)
    def visit(self, node: AST.WhileStatement):
        self.memory.push_memory_to_stack()

        while self.visit(node.expression):
            self.visit(node.statement)
        
        self.memory.pop_memory_from_stack()

    @when(AST.ForStatement)
    def visit(self, node: AST.ForStatement):
        self.memory.push_memory_to_stack()

        list_to_iterate = self.visit(node.elementsOrRange)

        for el in list_to_iterate:
            self.memory.set_variable(self.visit(node.identifier), el)
            self.visit(node.statement)

        self.memory.pop_memory_from_stack()

    @when(AST.SelectionStatement)
    def visit(self, node: AST.SelectionStatement):
        self.memory.push_memory_to_stack()

        if self.visit(node.expression):
            self.visit(node.statement_true)
        elif node.statement_false != None:
            self.visit(node.statement_false)

        self.memory.pop_memory_from_stack()

    @when(AST.BinaryOperation)
    def visit(self, node: AST.BinaryOperation):
        left = self.visit(node.left_expression)
        right = self.visit(node.right_expression)

        if node.operator == "+":
            return left + right
        elif node.operator == "-":
            return left - right
        elif node.operator == "*":
            return left * right
        elif node.operator == "/":
            return left / right
        elif node.operator == ".+":
            return left + right
        elif node.operator == ".-":
            return left - right
        elif node.operator == ".*":
            return np.multiply(left, right)
        elif node.operator == "./":
            return np.divide(left, right)
        elif node.operator == "==":
            return left == right
        elif node.operator == "!=":
            return left != right
        elif node.operator == ">=":
            return left >= right
        elif node.operator == "<=":
            return left <= right
        elif node.operator == "<":
            return left < right
        elif node.operator == ">":
            return left > right

    @when(AST.Primitive)
    def visit(self, node: AST.Primitive):
        return self.visit(node.value) if isinstance(node.value, AST.Number) else node.value

    @when(AST.Number)
    def visit(self, node: AST.Number):
        return node.value

    @when(AST.LValue)
    def visit(self, node: AST.LValue):
        return self.memory.get_variable(node.name)

    @when(AST.Range)
    def visit(self, node: AST.Range):
        return np.arange(
                    self.visit(node.from_expression),
                    self.visit(node.to_expression),
                    self.visit(node.step_expression),
                )

    @when(AST.MatrixFunction)
    def visit(self, node: AST.MatrixFunction):
        size = self.visit(node.size)
        if node.function == 'zeros':
            return np.zeros((size, size))
        elif node.function == 'ones':
            return np.ones((size, size))
        elif node.function == 'eye':
            return np.eye(size)

    @when(AST.RangeElement)
    def visit(self, node: AST.RangeElement):
        if isinstance(node.value, str):
            return self.memory.get_variable(node.value)
            
        return self.visit(node.value)

    @when(AST.Vector)
    def visit(self, node: AST.Vector):
        return list(map(lambda el: self.visit(el), node.content))

    @when(AST.LabelNode)
    def visit(self, node: AST.LabelNode):
        return node.name

