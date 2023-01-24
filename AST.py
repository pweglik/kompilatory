from abc import ABC, abstractmethod
from typing import Union

class Node(ABC):
    count = 0

    def __init__(self):
        self.id = str(Node.count)
        Node.count += 1

    @abstractmethod
    def print(self, indent=0):
        pass


class StatementList(
    Node,
):
    def __init__(self, statements, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.statements = statements

    def print(self, indent=0):
        for statement in self.statements:
            statement.print(indent)


class SelectionStatement(Node):
    def __init__(
        self, expression, statement_true, statement_false=None, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.expression = expression
        self.statement_true = statement_true
        self.statement_false = statement_false

    def print(self, indent=0):
        print("| " * indent + "if")
        self.expression.print(indent + 1)
        self.statement_true.print(indent + 1)
        if self.statement_false:
            self.statement_false.print(indent + 1)


class WhileStatement(Node):
    def __init__(self, expression, statement, line_number):
        super().__init__()
        self.line_number = line_number

        self.expression = expression
        self.statement = statement

    def print(self, indent=0):
        print("| " * indent + "while")
        self.expression.print(indent + 1)
        self.statement.print(indent + 1)


class ForStatement(Node):
    def __init__(self, identifier, elementsOrRange, statement, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.identifier = identifier  # ID string
        self.elementsOrRange = elementsOrRange
        self.statement = statement

    def print(self, indent=0):
        print("| " * indent + "for")
        self.identifier.print(indent + 1)
        self.elementsOrRange.print(indent + 1)
        self.statement.print(indent + 1)


class LabelNode(Node):
    def __init__(self, name, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.name = name

    def print(self, indent=0):
        print("| " * indent + str(self.name))


class JumpStatement(Node):
    def __init__(self, name, expression=None, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.name = name
        self.expression = expression

    def print(self, indent=0):
        print("| " * indent + self.name)


class PrintStatement(Node):
    def __init__(self, expression, line_number):
        self.line_number = line_number

        self.expression = expression

    def print(self, indent=0):
        print("| " * indent + "print")
        self.expression.print(indent + 1)


class Vector(Node):
    def __init__(self, content, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.content = content

    def print(self, indent=0):
        print("| " * indent + "vector")
        for elem in self.content:
            if isinstance(elem, Node):
                elem.print(indent + 1)
            else:
                print("| " * (indent + 1) + str(elem))


class LValue(Node):
    def __init__(self, id, list_access: Union[Vector, None]=None, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.name = id
        self.list_access = list_access

    def print(self, indent=0):
        print("| " * indent + self.name)
        if self.list_access:
            self.list_access.print(indent)


class AssignmentStatement(Node):
    def __init__(
        self, identifier: LValue, ass_operator: str, expression, line_number: int
    ):
        super().__init__()
        self.line_number = line_number

        self.identifier = identifier
        self.ass_operator = ass_operator
        self.expression = expression

    def __str__(self):
        return f"{self.identifier}={self.expression}"

    def print(self, indent=0):
        print("| " * indent + str(self.ass_operator))
        self.identifier.print(indent + 1)
        self.expression.print(indent + 1)


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
    def __init__(self, left_expression, operator, right_expression, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.left_expression = left_expression
        self.operator = operator
        self.right_expression = right_expression

    def print(self, indent=0):
        print("| " * indent + self.operator)
        self.left_expression.print(indent + 1)
        self.right_expression.print(indent + 1)


class UnaryMinusOperation(Node):
    def __init__(self, expression, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.expression = expression

    def print(self, indent=0):
        print("| " * indent + "-")
        self.expression.print(indent + 1)


class TransposedExpression(Node):
    def __init__(self, expression, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.expression = expression

    def print(self, indent=0):
        print("| " * indent + "transposed")
        self.expression.print(indent + 1)


class Range(Node):
    def __init__(
        self, from_expression, to_expression, step_expression=None, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.from_expression = from_expression
        self.to_expression = to_expression
        self.step_expression = (
            step_expression if step_expression else RangeElement(Number(1))
        )

    def print(self, indent=0):
        print("| " * indent + "range")
        self.from_expression.print(indent + 1)
        self.to_expression.print(indent + 1)
        self.step_expression.print(indent + 1)


class RangeElement(Node):
    def __init__(self, value, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.value = value

    def print(self, indent=0):
        if type(self.value) == str:
            print("| " * indent + str(self.value))
        else:
            self.value.print(indent)


class Primitive(Node):
    def __init__(self, value, line_number=None):
        super().__init__()
        self.line_number = line_number

        if isinstance(value, int) or isinstance(value, float):
            self.value = Number(value=value)
            return

        self.value = value

    def print(self, indent=0):
        print(
            "| " * indent + str(self.value.value)
            if isinstance(self.value, Number)
            else f'"{self.value}"'
        )


class MatrixFunction(Node):
    def __init__(self, function, size, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.function = function
        self.size = size

    def print(self, indent=0):
        print("| " * indent + f"{self.function}")
        self.size.print(indent + 1)


class Number(Node):
    def __init__(self, value, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.value = value

    def print(self, indent=0):
        print("| " * indent + str(self.value))
