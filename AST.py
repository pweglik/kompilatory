from abc import ABC, abstractmethod
import pydot

class Node(ABC):
    count = 0
    def __init__(self):
        self.id = str(Node.count)
        Node.count += 1
        

    @abstractmethod
    def print(self, indent=0):
        pass

    @abstractmethod
    def graph(self, dot):
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

    def graph(self, dot):
        main_node = pydot.Node(self.id, label="StatementList", shape="ellipse")
        dot.add_node(main_node)
        for i, statement in enumerate(self.statements):
            node = statement.graph(dot)
            dot.add_node(node)
            edge = pydot.Edge(self.id, statement.id, label=i)
            dot.add_edge(edge)
        return main_node


class Statement(Node):
    def __init__(self, statement, line_number=None):
        self.line_number = line_number

        self.statement = statement

    def print(self, indent=0):
        self.statement.print(indent)


class SelectionStatement(Node):
    def __init__(self, expression, statement_true, statement_false, line_number):
        self.line_number = line_number

        self.expression = expression
        self.statement_true = statement_true
        self.statement_false = statement_false


class IterationStatement(Node):
    def __init__(self, expression, statement, items, line_number):
        self.line_number = line_number

        self.expression = expression
        self.items = items
        self.statement = statement

class ForStatement(Node):
    def __init__(self, identifier, elements, statement, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.identifier = identifier # ID string
        self.elements = elements
        self.statement = statement

    def print(self, indent=0):
        print("| " * indent + "for")
        print("| " * (indent + 1) +  str(self.identifier))
        # self.identifier.print(indent + 1)
        self.elements.print(indent + 1)
        self.statement.print(indent + 1)

    def graph(self, dot):
        main_node = pydot.Node(self.id, label="for", shape="ellipse")
        dot.add_node(main_node)
        # node1 = pydot.Node(self.identifier 
        # id = self.identifier
        # node1 = pydot.Node('0'+self.id, label=self.identifier, shape="ellipse")
        node2 = self.elements.graph(dot)
        node3 = self.statement.graph(dot)
        # edge1 = pydot.Edge(self.id, self.identifier.id, label=0)
        edge2 = pydot.Edge(self.id, self.elements.id, label=1)
        edge3 = pydot.Edge(self.id, self.statement.id, label=2)
        # dot.add_edge(edge1)
        dot.add_edge(edge2)
        dot.add_edge(edge3)
        return main_node




class JumpStatement(Node):
    def __init__(self, line_number):
        self.line_number = line_number


class PrintStatement(Node):
    def __init__(self, expression, line_number):
        self.line_number = line_number

        self.expression = expression


class AssignmentStatement(Node):
    def __init__(self, identifier, ass_operator, expression, line_number):
        super().__init__()
        self.line_number = line_number

        self.identifier = identifier
        self.ass_operator = ass_operator
        self.expression = expression

    def __str__(self):
        return f"{self.identifier}={self.expression}"

    def print(self, indent=0):
        print("| " * indent, self.ass_operator)
        self.identifier.print(indent + 1)
        self.expression.print(indent + 1)

    def graph(self, dot):


        main_node = pydot.Node(self.id, label=self.ass_operator, shape="ellipse")
        dot.add_node(main_node)
        node1 = self.identifier.graph(dot)
        node2 = self.expression.graph(dot)
        edge1 = pydot.Edge(self.id, self.identifier.id, label=0)
        edge2 = pydot.Edge(self.id, self.expression.id, label=1)
        dot.add_edge(edge1)
        dot.add_edge(edge2)
        return main_node



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
        super().__init__()
        self.line_number = line_number

        self.first_expression = first_expression
        self.operator = operator
        self.second_expression = second_expression

    # def __str__(self):
    #     return f'{self.operator}{self.first_expression}{self.second_expression}'

    def print(self, indent=0):
        print('| '*indent+self.operator)
        self.first_expression.print(indent + 1)
        self.second_expression.print(indent + 1)

    def graph(self, dot):
        node = pydot.Node(self.id, label=self.operator, shape='ellipse')
        dot.add_node(node)
        node1 = self.first_expression.graph(dot)
        node2 = self.second_expression.graph(dot)
        edge1 = pydot.Edge(self.id, self.first_expression.id, label=0)
        edge2 = pydot.Edge(self.id, self.second_expression.id, label=1)
        dot.add_edge(edge1)
        dot.add_edge(edge2)
        return node


class UnaryMinusOperation(Node):
    def __init__(self, expression, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.expression = expression

    def print(self, indent=0):
        print("| " * indent + "-")
        self.expression.print(indent + 1)

    def graph(self, dot):
        node = pydot.Node(self.id, label="-", shape="ellipse")
        dot.add_node(node)
        node1 = self.expression.graph(dot)
        edge = pydot.Edge(self.id, self.expression.id, label=0)
        dot.add_edge(edge)
        return node


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
    def __init__(self, from_el, to_el, step_el=1, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.from_el = from_el
        self.to_el = to_el
        self.step_el = step_el

    def print(self, indent=0):
        print("| " * indent + "range")
        # print("| " * (indent + 1) + str(self.from_el))
        self.from_el.print(indent + 1)
        # print("| " * (indent + 1) + str(self.to_el))
        self.to_el.print(indent + 1)
        # self.step_el.print(indent + 1)
        #TODO: check

    def graph(self, dot):
        node = pydot.Node(self.id, label="range", shape="ellipse")
        dot.add_node(node)
        # node1 = self.from_el.graph(dot)
        # node2 = self.to_el.graph(dot)
        # node3 = self.step_el.graph(dot)
        # edge1 = pydot.Edge(self.id, self.from_el.id, label=0)
        # edge2 = pydot.Edge(self.id, self.to_el.id, label=1)
        # edge3 = pydot.Edge(self.id, self.step_el.id, label=2)
        # dot.add_edge(edge1)
        # dot.add_edge(edge2)
        # dot.add_edge(edge3)
        return node
        # TODO: check


class RangeElement(Node):
    def __init__(self, value, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.value = value

    def print(self, indent=0):
        # print("| " * indent + str(self.value))
        self.value.print(indent + 1)

    def graph(self, dot):
        node = pydot.Node(self.id, label=str(self.value), shape="ellipse")
        dot.add_node(node)
        return node


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


class LValue(Node):
    def __init__(self, id, list_access=None, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.name = id
        self.list_access = list_access

    # def __str__(self):
    #     return self.id

    def print(self, indent=0):
        if self.list_access:
            self.list_access.print(indent)
        print("| " * indent + self.name)

    def graph(self, dot):
        node = pydot.Node(self.id, label=self.name, shape='ellipse')
        dot.add_node(node)
        return node


class Number(Node):
    def __init__(self, value, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.value = value

    # def __str__(self):
    #     return str(self.value)

    def print(self, indent=0):
        print("| " * indent + str(self.value))

    def graph(self, dot):
        node = pydot.Node(self.id, label=self.value, shape='ellipse')
        dot.add_node(node)
        return node
