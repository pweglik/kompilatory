class Node:
    pass

class LValue(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value

class LValue(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value

class LValue(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value

class LValue(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value

class Continue(Node):
    def __init__(self, line_number=None):
        self.line_number = line_number

class Break(Node):
    def __init__(self, line_number=None):
        self.line_number = line_number

class Return(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value

class Print(Node):
    def __init__(self, content, line_number=None):
        self.line_number = line_number

        self.content = content


class BinaryOperation(Node):
    def __init__(self, first_expression, operator, second_expression, line_number=None):
        self.line_number = line_number

        self.first_expression = first_expression
        self.operator = operator
        self.second_expression = second_expression

class UnaryMinusOperation(Node):
    def __init__(self, expression, line_number=None):
        self.line_number = line_number

        self.expression = expression

class TransposedExpression(Node):
    def __init__(self, expression, line_number=None):
        self.line_number = line_number

        self.expression = expression

class ListAccess(Node):
    def __init__(self, element, next_list_access, line_number=None):
        self.line_number = line_number

        self.element = element
        self.next_list_access = next_list_access

class ListAccessElement(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value

class Range(Node):
    def __init__(self, from_el, to_el, step_el, line_number=None):
        self.line_number = line_number

        self.from_el = from_el
        self.to_el = to_el
        self.step_el = step_el


class RangeElement(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value

class List(Node):
    def __init__(self, content, line_number=None):
        self.line_number = line_number

        self.content = content

class ListContent(Node):
    def __init__(self, expression, next_list_content, line_number=None):
        self.line_number = line_number

        self.expression = expression
        self.next_list_content = next_list_content

class Primitive:
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value

class MatrixFunctions(Node):
    def __init__(self, function, size, line_number=None):
        self.line_number = line_number

        self.function = function
        self.size = size

class AssignmentStatement(Node):
    def __init__(self, l_value, ass_operator, expression, line_number=None):
        self.line_number = line_number

        self.l_value = l_value
        self.ass_operator = ass_operator
        self.expression = expression

class LValue(Node):
    def __init__(self, id, list_access=None, line_number=None):
        self.line_number = line_number

        self.id = id
        self.list_access = list_access

class Number(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value
