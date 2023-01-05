class Node:
    pass

class StatementList(Node):
    def __init__(self, statements, line_number):
        self.statements = statements
        self.line_number = line_number

class Statement(Node):
    def __init__(self, statement, line_number):
        self.statement = statement
        self.line_number = line_number


class SelectionStatement(Node):
    def __init__(self, expression, statement_true, statement_false, line_number):
        self.expression = expression
        self.statement_true = statement_true
        self.statement_false = statement_false
        self.line_number = line_number

class IterationStatement(Node):
    def __init__(self, expression, statement, items, line_number):
        self.expression = expression
        self.items = items
        self.statement = statement
        self.line_number = line_number
    
class JumpStatement(Node):
    def __init__(self, line_number):
        self.line_number = line_number


class PrintStatement(Node):
    def __init__(self, expression, line_number):
        self.expression = expression
        self.line_number = line_number

class AssignmentStatement(Node):
    def __init__(self, identifier, expression, line_number):
        self.identifier = identifier
        self.expression = expression
        self.line_number = line_number
