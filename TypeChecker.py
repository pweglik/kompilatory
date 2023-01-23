#!/usr/bin/env python3

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
    else:
        return None


class NodeVisitor(object):
    def visit(self, node: AST.Node):
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
        type_ = self.visit(node.expression)
        if self.symbol_table.get(node.identifier.name) is None:
            self.symbol_table.put(node.identifier.name, VarSymbol(
                node.identifier.name, type_
            ))
        else:
            if self.symbol_table.get(node.identifier.name).type_ != type_:
                self.errors.append(
                    f"Type mismatch in line {node.line_number} : {self.symbol_table.dict[node.identifier.name].type_} = {type_}"
                )

    def visit_LValue(self, node):
        if not self.symbol_table.get(node.name) is None:
            return self.symbol_table.get(node.name).type_
        else:
            self.errors.append(
                f"Variable {node.name} not declared in line {node.line_number} "
            )
            return None

    def visit_Number(self, node):
        return type_to_str(node.value)

    def visit_Primitive(self, node):
        if isinstance(node.value, AST.Node):
            return self.visit(node.value)
        else:
            return "string"

    def visit_MatrixFunction(self, node):
        visit_type = self.visit(node.size)
        if visit_type != "int":
            self.errors.append(
                f"Matrix size must be an integer but is {visit_type} in line {node.line_number}"
            )

        return "vector"

    def visit_Vector(self, node):
        content = node.content


        if content is None:
            return None
        if isinstance(content, list):
            size = len(content)
        

        if size > 0:
            types = []
            for element in content:
                if isinstance(element, AST.Node):
                    element_type = self.visit(element)
                else:
                    element_type = type_to_str(element)
                types += [element_type]

            print(types)
            print(set(types))
            if len(set(types)) == 1:
                type_ = types[0]
                if type_ in ["int", "float", "string"]:
                    return "vector", [size]
                else:
                    return "vector",[size]+type_[1]
            else:
                self.errors.append(
                    f"Type mismatch in line {node.line_number} : {types}. Values in vector should be of the same type."
                )
                return None
            

    def visit_BinaryOperation(self, node):
        left_type = self.visit(node.left_expression)
        right_type = self.visit(node.right_expression)

        if left_type is None or right_type is None:
            return None

        if left_type == right_type:
            return left_type
        else:
            try:
                return type_map[node.op][left_type][right_type]
            except KeyError:
                self.errors.append(
                    f"Type mismatch in line {node.line_number} : {left_type} {node.op} {right_type}"
                )
                return None
