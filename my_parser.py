#!/usr/bin/python

from lexer import SimpleLexer
from sly import Parser
import AST

scanner_obj = SimpleLexer()


class SimpleParser(Parser):
    tokens = SimpleLexer.tokens
    debugfile = "debug.log"

    precedence = (
        ("nonassoc", IF_PREC),
        ("nonassoc", ELSE),
        ("nonassoc", ASS, ASS_ADD, ASS_SUB, ASS_DIV, ASS_MUL),
        ("nonassoc", EQ, LESS_EQ, GREATER_EQ, NOT_EQ, GREATER, LESS),
        ("left", ADD, SUB, ADD_EL, SUB_EL),
        ("left", MUL, DIV, MUL_EL, DIV_EL),
        ("right", UMINUS),
        ("left", MAT_TRANS),
    )

    @_("Statement StatementList")
    def StatementList(self, p):
        p[1].statements.insert(0, p[0])
        return p[1]

    @_("Statement")
    def StatementList(self, p):
        return AST.StatementList(statements=[p[0]])

    @_(
        "CompoundStatement",
        "SelectionStatement",
        "IterationStatement",
        'JumpStatement ";"',
        'PrintStatement ";"',
        'AssignmentStatement ";"',
        'Expression ";"',
    )
    def Statement(self, p):
        return p[0]

    @_('"{" StatementList "}"')
    def CompoundStatement(self, p):
        return p[1]

    @_('IF "(" Expression ")" Statement %prec IF_PREC')
    def SelectionStatement(self, p):
        return AST.SelectionStatement(expression=p[2], statement_true=p[4], line_number=p.lineno)

    @_('IF "(" Expression ")" Statement ELSE Statement')
    def SelectionStatement(self, p):
        return AST.SelectionStatement(expression=p[2], statement_true=p[4], statement_false=p[6], line_number=p.lineno)

    @_('WHILE "(" Expression ")" Statement')
    def IterationStatement(self, p):
        return AST.WhileStatement(expression=p[2], statement=p[4], line_number=p.lineno)

    @_("FOR ID ASS Range Statement", "FOR ID ASS List Statement")
    def IterationStatement(self, p):
        iterator = AST.LabelNode(name=p[1], line_number=p.lineno)
        return AST.ForStatement(
            identifier=iterator, elements=p[3], statement=p[4], line_number=p.lineno
        )

    @_("BREAK", "CONTINUE")
    def JumpStatement(self, p):
        # return p[0].upper()
        return AST.JumpStatement(name=p[0].upper(), line_number=p.lineno)

    @_("RETURN Expression")
    def JumpStatement(self, p):
        return AST.JumpStatement(name=p[0].upper(), expression=p[1], line_number=p.lineno)

    @_("PRINT ListContent")
    def PrintStatement(self, p):
        return "PRINT", p[1]

    @_(
        "Expression ADD Expression",
        "Expression SUB Expression",
        "Expression MUL Expression",
        "Expression DIV Expression",
        "Expression ADD_EL Expression",
        "Expression SUB_EL Expression",
        "Expression MUL_EL Expression",
        "Expression DIV_EL Expression",
        "Expression EQ Expression",
        "Expression NOT_EQ Expression",
        "Expression LESS_EQ Expression",
        "Expression GREATER_EQ Expression",
        "Expression GREATER Expression",
        "Expression LESS Expression",
    )
    def Expression(self, p):
        return AST.BinaryOperation(p[0], p[1], p[2])

    @_(
        '"(" Expression ")"',
    )
    def Expression(self, p):
        return p[1]

    @_(
        "SUB Expression %prec UMINUS",
    )
    def Expression(self, p):
        return AST.UnaryMinusOperation(p[1], line_number=p.lineno)

    @_("Expression MAT_TRANS")
    def Expression(self, p):
        return ("TRANSPOSE", p[0])

    @_("List", "Primitive", "LValue", "MatrixFunction")
    def Expression(self, p):
        return p[0]

    @_('"[" ListAccessElement "]"')
    def ListAccess(self, p):
        return [p[1]]

    @_('"[" ListAccessElement "]" ListAccess')
    def ListAccess(self, p):
        return [p[1]] + p[3]

    @_("INT", "ID")
    def ListAccessElement(self, p):
        return p[0]

    @_('RangeElement ":" RangeElement')
    def Range(self, p):
        return AST.Range(from_el=p[0], to_el=p[2], line_number=p[0].line_number)

    @_('RangeElement ":" RangeElement ":" RangeElement')
    def Range(self, p):
        return ("Range", p[0], p[2], p[4])

    @_("Number")
    def RangeElement(self, p):
        element = AST.RangeElement(value=p[0], line_number=p[0].line_number)
        return element

    @_("ID")
    def RangeElement(self, p):
        element = AST.RangeElement(value=p[0], line_number=p.lineno)
        return element

    @_('"[" ListContent "]"')
    def List(self, p):
        return AST.List(content=p[1])

    @_('Expression "," ListContent')
    def ListContent(self, p):
        return AST.ListContent(expression=p[0], next_list_content=p[2])

    @_("Expression")
    def ListContent(self, p):
        return AST.ListContent(expression=p[0])

    @_("Number", "STRING")
    def Primitive(self, p):
        return AST.Primitive(value=p[0])

    @_('ZEROS "(" Expression ")"', 'ONES "(" Expression ")"', 'EYE "(" Expression ")"')
    def MatrixFunction(self, p):
        return AST.MatrixFunction(p[0], p[2])

    @_("LValue ASS Expression")
    def AssignmentStatement(self, p):
        return AST.AssignmentStatement(
            identifier=p[0],
            ass_operator="=",
            expression=p[2],
            line_number=p[0].line_number,
        )

    @_(
        "LValue ASS_ADD Expression",
        "LValue ASS_SUB Expression",
        "LValue ASS_DIV Expression",
        "LValue ASS_MUL Expression",
    )
    def AssignmentStatement(self, p):
        return AST.AssignmentStatement(
            identifier=p[0],
            ass_operator=p[1],
            expression=p[2],
            line_number=p[0].line_number,
        )

    @_("ID")
    def LValue(self, p):
        return AST.LValue(p[0], line_number=p.lineno)

    @_("ID ListAccess")
    def LValue(self, p):
        return AST.LValue(p[0], p[1], line_number=p.lineno)

    @_("INT", "FLOAT")
    def Number(self, p):
        return AST.Number(p[0], p.lineno)
