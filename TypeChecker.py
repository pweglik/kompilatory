#!/usr/bin/env python3

from typing import Union
import AST
from SymbolTable import *
from collections import defaultdict


type_map = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

type_map["+"]["int"]["int"] = "int"
type_map["+"]["int"]["float"] = "float"
type_map["+"]["float"]["int"] = "float"
type_map["+"]["float"]["float"] = "float"
type_map["+"]["string"]["string"] = "string"

type_map["-"]["int"]["int"] = "int"
type_map["-"]["int"]["float"] = "float"
type_map["-"]["float"]["int"] = "float"
type_map["-"]["float"]["float"] = "float"

type_map["*"]["int"]["int"] = "int"
type_map["*"]["int"]["float"] = "float"
type_map["*"]["float"]["int"] = "float"
type_map["*"]["float"]["float"] = "float"

type_map["/"]["int"]["int"] = "int"
type_map["/"]["int"]["float"] = "float"
type_map["/"]["float"]["int"] = "float"
type_map["/"]["float"]["float"] = "float"

type_map["<"]["int"]["int"] = "bool"
type_map["<"]["int"]["float"] = "bool"
type_map["<"]["float"]["int"] = "bool"
type_map["<"]["float"]["float"] = "bool"

type_map[">"]["int"]["int"] = "bool"
type_map[">"]["int"]["float"] = "bool"
type_map[">"]["float"]["int"] = "bool"
type_map[">"]["float"]["float"] = "bool"

type_map["<="]["int"]["int"] = "bool"
type_map["<="]["int"]["float"] = "bool"
type_map["<="]["float"]["int"] = "bool"
type_map["<="]["float"]["float"] = "bool"

type_map[">="]["int"]["int"] = "bool"
type_map[">="]["int"]["float"] = "bool"
type_map[">="]["float"]["int"] = "bool"
type_map[">="]["float"]["float"] = "bool"

type_map["=="]["int"]["int"] = "bool"
type_map["=="]["int"]["float"] = "bool"
type_map["=="]["float"]["int"] = "bool"
type_map["=="]["float"]["float"] = "bool"
type_map["=="]["bool"]["bool"] = "bool"
type_map["=="]["string"]["string"] = "bool"

type_map["!="]["int"]["int"] = "bool"
type_map["!="]["int"]["float"] = "bool"
type_map["!="]["float"]["int"] = "bool"
type_map["!="]["float"]["float"] = "bool"
type_map["!="]["bool"]["bool"] = "bool"
type_map["!="]["string"]["string"] = "bool"

type_map[".+"]["vector"]["vector"] = "vector"

type_map[".-"]["vector"]["vector"] = "vector"

type_map[".*"]["vector"]["vector"] = "vector"
type_map[".*"]["vector"]["int"] = "vector"
type_map[".*"]["vector"]["float"] = "vector"
type_map[".*"]["int"]["vector"] = "vector"
type_map[".*"]["float"]["vector"] = "vector"

type_map["./"]["vector"]["vector"] = "vector"
type_map["./"]["vector"]["int"] = "vector"
type_map["./"]["vector"]["float"] = "vector"


def type_to_str(elem):
    if type(elem) == str:
        return "string"
    elif type(elem) == int:
        return "int"
    elif type(elem) == float:
        return "float"
    elif isinstance(elem, VarSymbol):
        return elem.type


class NodeVisitor(object):
    def visit(self, node: AST.Node) -> Union[VarSymbol, None]:
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: AST.Node):
        print("generic_visit", node.__class__.__name__)


class TypeChecker(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable(None, "main")
        self.loopcount = 0
        self.errors = []

    def visit_StatementList(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_SelectionStatement(self, node):
        self.visit(node.expression)
        self.visit(node.statement)

        if node.else_statement is not None:
            self.visit(node.else_statement)

    def visit_WhileStatement(self, node):
        self.loopcount += 1

        self.symbol_table = self.symbol_table.pushScope("While")
        self.visit(node.expression)
        self.visit(node.statement)

        self.loopcount -= 1
        self.symbol_table = self.symbol_table.popScope()

    def visit_ForStatement(self, node):
        self.loopcount += 1

        self.symbol_table = self.symbol_table.pushScope("For")
        self.visit(node.elements)
        # TODO range and list type
        self.symbol_table.dict[node.identifier.name] = VarSymbol(
            node.identifier.name, node.type_
        )

        self.visit(node.statement)

        self.loopcount -= 1
        self.symbol_table = self.symbol_table.popScope()

    def visit_LabelNode(self, node):
        self.visit(node.statement)

    def visit_JumpStatement(self, node):
        if node.name == "BREAK" or node.name == "CONTINUE":
            if self.loopcount == 0:
                self.errors.append(
                    f"Break/Continue outside of loop in line {node.line_number}"
                )

    def visit_AssignmentStatement(self, node):
        symbol = self.visit(node.expression)
        if symbol == None:
            raise ValueError("Expression isit return None instead of VarSymbol!")

        exisiting_symbol = self.symbol_table.get(node.identifier.name)
        if exisiting_symbol is None:
            self.symbol_table.put(
                node.identifier.name, symbol
            )
        else:
            if exisiting_symbol.type_ != symbol.type_:
                self.errors.append(
                    f"Type mismatch in line {node.line_number} : {self.symbol_table.dict[node.identifier.name].type_} = {type_}"
                )

    def visit_LValue(self, node):
        if not self.symbol_table.get(node.name) is None:
            return self.symbol_table.get(node.name)
        else:
            self.errors.append(
                f"Variable {node.name} not declared in line {node.line_number} "
            )
            return None

    def visit_Number(self, node):
        print(type(node.value))
        print(type_to_str(node.value))

        return VarSymbol(None, type_=type_to_str(node.value))

    def visit_Primitive(self, node):
        if isinstance(node.value, AST.Node):
            return self.visit(node.value)
        else:
            return VarSymbol(None, type_to_str(node))

    def visit_MatrixFunction(self, node):
        self.visit(node.size)
        return VarSymbol(None, "vector", (node.size, node.size))

    def visit_Vector(self, node):
        content = node.content
        size = len(content)

        if size > 0:
            types = []
            for element in content:
                if isinstance(element, AST.Node):
                    element_type = self.visit(element)
                else:
                    element_type = VarSymbol(None, type_to_str(element))
                types += [element_type]

            if all(x == types[0] for x in types):
                if isinstance(types[0], VarSymbol):
                    if types[0].shape is None:
                        return VarSymbol(None, "vector", (size,))
                    else:
                        return VarSymbol(None, "vector", (size,) + types[0].shape)
                else:
                    return VarSymbol(None, "vector", (size,))
            else:
                self.errors.append(
                    f"Vector must have same type elements in line {node.line_number}"
                )
                return None

    def visit_BinaryOperation(self, node):
        left_symbol = self.visit(node.left_expression)
        right_symbol = self.visit(node.right_expression)
        
        if left_symbol is None or right_symbol is None:
            return None
        
        if left_symbol.type_ == "vector" and right_symbol.type_ == "vector":
            # TODO HERE
            if left_symbol.shape == right_symbol.shape:
                return VarSymbol(None, "vector", left_symbol.shape)
            else:
                self.errors.append(
                    f"Vector shapes must be the same in line {node.line_number}"
                )
                return None
        return VarSymbol(None, type_map[left_symbol.type_][node.operator][right_symbol.type_])
