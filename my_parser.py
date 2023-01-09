#!/usr/bin/python

from lexer import SimpleLexer
from sly import Parser
import AST

scanner_obj = SimpleLexer()

class SimpleParser(Parser):
    tokens = SimpleLexer.tokens
    verbose = False
    debugfile='debug.log'

    precedence = (
        ('nonassoc', IF_PREC),
        ('nonassoc', ELSE),
        ('nonassoc', ASS, ASS_ADD, ASS_SUB, ASS_DIV, ASS_MUL),
        ('nonassoc', EQ, LESS_EQ, GREATER_EQ, NOT_EQ, GREATER, LESS),
        ('left', ADD, SUB, ADD_EL, SUB_EL),
        ('left', MUL, DIV, MUL_EL, DIV_EL),
        ('right', UMINUS),
        ('left', MAT_TRANS),
    )


    @_('Statement StatementList')
    def StatementList(self, p):
        if self.verbose:
            print("StatementList", p[0], p[1])

        # return [("Statement",p[0])] + p[1]
        p[1].statements.insert(0, p[0])
        return p[1]


    @_('Statement')
    def StatementList(self, p):
        if self.verbose:
            print("StatementList", p[0])
        # return [("Statement", p[0])]
        return AST.StatementList(statements=[p[0]])

    @_('CompoundStatement',
        'SelectionStatement',
        'IterationStatement',
        'JumpStatement ";"',
        'PrintStatement ";"',
        'AssignmentStatement ";"',
        'Expression ";"')
    def Statement(self, p):
        # print("lala", p.lineno, p[0])
        if self.verbose:
            print("Statement", p[0])
        return p[0]

    
    @_('"{" StatementList "}"')
    def CompoundStatement(self, p):
        if self.verbose:
            print("CompoundStatement", p[1])
        return p[1]

    @_('IF "(" Expression ")" Statement %prec IF_PREC')
    def SelectionStatement(self, p):
        if self.verbose:
            print("SelectionStatement", p[2], p[4])
        return "IF_TAG",(("IF", p[2]), ("THEN", p[4]))
    
    @_('IF "(" Expression ")" Statement ELSE Statement')
    def SelectionStatement(self, p):
        return "IF_ELSE_TAG", (("IF", p[2]), ("THEN", p[4]), ("ELSE", p[6]))


    @_('WHILE "(" Expression ")" Statement')
    def IterationStatement(self, p):
        if self.verbose:
            print("IterationStatement", p[0], p[1], p[2], p[3], p[4])
        return 'WHILE', p[2], p[4]

    @_('FOR ID ASS Range Statement',
        'FOR ID ASS List Statement')
    def IterationStatement(self, p):
        # return 'FOR', p[1], p[2], p[3], p[4]
        iterator = AST.LabelNode(name=p[1], line_number=p.lineno)
        return AST.ForStatement(identifier=iterator, elements=p[3], statement=p[4], line_number=p.lineno)


    @_('BREAK',
        'CONTINUE')
    def JumpStatement(self, p):
        if self.verbose:
            print("JumpStatement", p[0])
        return p[0].upper()

    @_('RETURN Expression')
    def JumpStatement(self, p):
        if self.verbose:
            print("JumpStatement", p[0], p[1])
        return p[0], p[1]


    @_('PRINT ListContent')
    def PrintStatement(self, p):
        if self.verbose:
            print("PrintStatement", p[1])
        return 'PRINT', p[1]

    @_(
        'Expression ADD Expression',
        'Expression SUB Expression',
        'Expression MUL Expression',
        'Expression DIV Expression',
        'Expression ADD_EL Expression',
        'Expression SUB_EL Expression',
        'Expression MUL_EL Expression',
        'Expression DIV_EL Expression',
        'Expression EQ Expression',
        'Expression NOT_EQ Expression',
        'Expression LESS_EQ Expression',
        'Expression GREATER_EQ Expression',
        'Expression GREATER Expression',
        'Expression LESS Expression',
        )
    def Expression(self, p):
        if self.verbose:
            print("Expression", p[0], p[1], p[2])
        # return (p[1], p[0], p[2])
        return AST.BinaryOperation(p[0], p[1], p[2])


    @_('"(" Expression ")"',)
    def Expression(self, p):
        if self.verbose:
            print("Expression", p[0], p[1], p[2])
        return p[1]


    @_('SUB Expression %prec UMINUS',
        )
    def Expression(self, p):
        if self.verbose:
            print('Expression', p[0], p[1])
        # return ('-', p[1])
        return AST.UnaryMinusOperation(p[1], line_number=p.lineno)


    @_('Expression MAT_TRANS')
    def Expression(self, p):
        if self.verbose:
            print('Expression', p[0], p[1])
        return ('TRANSPOSE', p[0])

    @_('List', 
    'Primitive', 
    'LValue', 
    'MatrixFunction')
    def Expression(self, p):
        if self.verbose:
            print('Expression', p[0])
        return p[0]

    @_('"[" ListAccessElement "]"')
    def ListAccess(self, p):
        if self.verbose:
            print("ListAccess", p[1])
        return ([p[1]])

    @_('"[" ListAccessElement "]" ListAccess')
    def ListAccess(self, p):
        if self.verbose:
            print("ListAccess", p[1], p[3])
        return ([p[1]] + p[3])

    @_('INT', 'ID')
    def ListAccessElement(self, p):
        if self.verbose:
            print("ListAccessElement", p[0])
        return p[0]

    @_('RangeElement ":" RangeElement')
    def Range(self, p):
        if self.verbose:
            print("Range", p[0], p[2])
        # return ("Range", p[0], p[2])
        return AST.Range(from_el=p[0], to_el=p[2], line_number=p[0].line_number)

    @_('RangeElement ":" RangeElement ":" RangeElement')
    def Range(self, p):
        if self.verbose:
            print("Range", p[0], p[2], p[4])
        return ("Range", p[0], p[2], p[4])

    @_('Number')
    def RangeElement(self, p):
        if self.verbose:
            print("RangeElement", p[0])
        # return p[0]
        element = AST.RangeElement(value=p[0], line_number=p[0].line_number)
        return element

    @_( 'ID')
    def RangeElement(self, p):
        if self.verbose:
            print("RangeElement", p[0])
        # return p[0]
        element = AST.RangeElement(value=p[0], line_number=p.lineno)
        return element

    @_('"[" ListContent "]"')
    def List(self, p):
        if self.verbose:
            print("List", p[1])
        return 'List', p[1]

    @_('Expression "," ListContent')
    def ListContent(self, p):
        if self.verbose:
            print("ListContent", p[0], p[2])

        # print(f'p[0]: {p[0]}\tp[1]: {p[2]}\t[p[0]]: {[p[0]]}\t[p[0]].extend(p[1]): {[p[0]].extend(p[1])}')
        return [p[0]]+p[2]

    @_('Expression')
    def ListContent(self, p):
        if self.verbose:
            print("ListContent", p[0])
        return [p[0]]

    @_('Number',
        'STRING')
    def Primitive(self, p):
        if self.verbose:
            print("Primitive", p[0])
        return p[0]

    @_('ZEROS "(" INT ")"',
        'ONES "(" INT ")"',
        'EYE "(" INT ")"')
    def MatrixFunction(self, p):
        if self.verbose:
            print("Matrix", p[0], p[2])
        return AST.MatrixFunction(p[0], p[2])

    @_('LValue ASS Expression')
    def AssignmentStatement(self, p):
        if self.verbose:
            print("AssignmentStatement", p[0], p[1], p[2])
        # return (p[1], p[0], p[2])
        return AST.AssignmentStatement(identifier=p[0], ass_operator='=', expression=p[2], line_number=p[0].line_number)

    @_('LValue ASS_ADD Expression',
    'LValue ASS_SUB Expression',
    'LValue ASS_DIV Expression',
    'LValue ASS_MUL Expression',)
    def AssignmentStatement(self, p):
        if self.verbose:
            print("AssignmentStatement", p[0], p[1], p[2])
        # return (p[1], p[0], p[2])
        return AST.AssignmentStatement(identifier=p[0], ass_operator=p[1], expression=p[2], line_number=p[0].line_number)

    @_('ID')
    def LValue(self, p):
        return AST.LValue(p[0], line_number=p.lineno)

    @_('ID ListAccess')
    def LValue(self, p):
        # return 'Access', p[0], p[1]
        return AST.LValue(p[0], p[1], line_number=p.lineno)

    @_('INT', 'FLOAT')
    def Number(self, p):
        if self.verbose:
            print("Number", p[0])
        # print(p.lineno)
        
        return AST.Number(p[0], p.lineno)
