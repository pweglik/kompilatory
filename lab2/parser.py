#!/usr/bin/python

from lexer import SimpleLexer
from sly import Parser


scanner_obj = SimpleLexer()

class SimpleParser(Parser):
    tokens = SimpleLexer.tokens
    verbose = False
    debugfile='debug.log'

    precedence = (
        ('nonassoc', EQ, LESS_EQ, GREATER_EQ, NOT_EQ, GREATER, LESS, IF_PREC, NO_MORE_LIST_ACCESS),
        ('nonassoc', ELSE, ASS, ASS_ADD, ASS_SUB, ASS_DIV, ASS_MUL),
        ('left', ADD, SUB, ADD_EL, SUB_EL),
        ('left', MUL, DIV, MUL_EL, DIV_EL),
        ('right', UMINUS),
        ('left', LIST_ACCESS, MAT_TRANS, MORE_LIST_ACCESS),
    )

    @_('StatementList')
    def Program(self, p):
        return ('Program', p[0])

    @_('Statement StatementList')
    def StatementList(self, p):
        if self.verbose:
            print("StatementList", p[0], p[1])
        return ("StatementList", p[0], p[1])

    @_('Statement')
    def StatementList(self, p):
        if self.verbose:
            print("StatementList", p[0])
        return ("StatementList", p[0])

    @_('CompoundStatement',
        'SelectionStatement',
        'IterationStatement',
        'JumpStatement ";"',
        'PrintStatement ";"',
        'AssignmentStatement ";"',
        'Expression ";"')
    def Statement(self, p):
        if self.verbose:
            print("Statement", p[0])
        return ("Statement", p[0])

    
    @_('"{" StatementList "}"')
    def CompoundStatement(self, p):
        if self.verbose:
            print("CompoundStatement", p[1])
        return ("CompoundStatement", p[1])

    @_('IF "(" Expression ")" Statement %prec IF_PREC')
    def SelectionStatement(self, p):
        if self.verbose:
            print("SelectionStatement", p[2], p[4])
        return ("SelectionStatement", p[2], p[4])
    
    @_('IF "(" Expression ")" Statement ELSE Statement')
    def SelectionStatement(self, p):
        if self.verbose:
            print("SelectionStatement", p[2], p[4], p[6])
        return ("SelectionStatement", p[2], p[4], p[6])

    @_('WHILE "(" Expression ")" Statement',
        'FOR ID ASS Range Statement',
        'FOR ID ASS List Statement')
    def IterationStatement(self, p):
        if self.verbose:
            print("IterationStatement", p[0], p[1], p[2], p[3], p[4])
        return ("IterationStatement", p[0], p[1], p[2], p[3], p[4])


    @_('BREAK',
        'CONTINUE')
    def JumpStatement(self, p):
        if self.verbose:
            print("JumpStatement", p[0])
        return ("JumpStatement", p[0])

    @_(
        'RETURN Expression')
    def JumpStatement(self, p):
        if self.verbose:
            print("JumpStatement", p[0], p[1])
        return ("JumpStatement", p[0], p[1])


    @_('PRINT ListContent')
    def PrintStatement(self, p):
        if self.verbose:
            print("PrintStatement", p[1])
        return ("PrintStatement", p[1])

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
        '"(" Expression ")"',
        )
    def Expression(self, p):
        if self.verbose:
            print("Expression", p[0], p[1], p[2])
        return ("Expression", p[0], p[1], p[2])


    @_('SUB Expression %prec UMINUS',
        'Expression MAT_TRANS',
        'Expression ListAccess'
        )
    def Expression(self, p):
        if self.verbose:
            print('Expression', p[0], p[1])
        return ('Expression', p[0], p[1])

    @_('List', 
    'Primitive', 
    'ID', 
    # 'ID %prec JUST_ID', 
    'MatrixFunctions')
    def Expression(self, p):
        if self.verbose:
            print('Expression', p[0])
        return ('Expression', p[0])

    @_('"[" ListAccessElement "]" %prec NO_MORE_LIST_ACCESS')
    def ListAccess(self, p):
        if self.verbose:
            print("ListAccess", p[1])
        return ("ListAccess", p[1])

    @_('"[" ListAccessElement "]" ListAccess %prec MORE_LIST_ACCESS')
    def ListAccess(self, p):
        if self.verbose:
            print("ListAccess", p[1], p[3])
        return ("ListAccess", p[1], p[3])

    @_('INT', 'ID')
    def ListAccessElement(self, p):
        if self.verbose:
            print("ListAccessElement", p[0])
        return ("ListAccessElement", p[0])

    @_('RangeElement ":" RangeElement')
    def Range(self, p):
        if self.verbose:
            print("Range", p[0], p[2])
        return ("Range", p[0], p[2])

    @_('RangeElement ":" RangeElement ":" RangeElement')
    def Range(self, p):
        if self.verbose:
            print("Range", p[0], p[2], p[4])
        return ("Range", p[0], p[2], p[4])

    @_('Number', 'ID')
    def RangeElement(self, p):
        if self.verbose:
            print("RangeElement", p[0])
        return ("RangeElement", p[0])

    @_('"[" ListContent "]"')
    def List(self, p):
        if self.verbose:
            print("List", p[1])
        return ("List", p[1])

    @_('Expression "," ListContent')
    def ListContent(self, p):
        if self.verbose:
            print("ListContent", p[0], p[2])
        return ("ListContent", p[0], p[2])

    @_('Expression')
    def ListContent(self, p):
        if self.verbose:
            print("ListContent", p[0])
        return ("ListContent", p[0])

    @_('Number',
        'STRING')
    def Primitive(self, p):
        if self.verbose:
            print("Primitive", p[0])
        return ('Primitive', p[0])

    @_('ZEROS "(" INT ")"',
        'ONES "(" INT ")"',
        'EYE "(" INT ")"')
    def MatrixFunctions(self, p):
        if self.verbose:
            print("Matrix", p[0], p[2])
        return ("Matrix", p[0], p[2])

    @_('ID ASS Expression',
    'ID ASS_ADD Expression',
    'ID ASS_SUB Expression',
    'ID ASS_DIV Expression',
    'ID ASS_MUL Expression',
    'ID ListAccess ASS Expression %prec LIST_ACCESS', 
    'ID ListAccess ASS_ADD Expression %prec LIST_ACCESS',
    'ID ListAccess ASS_SUB Expression %prec LIST_ACCESS',
    'ID ListAccess ASS_DIV Expression %prec LIST_ACCESS',
    'ID ListAccess ASS_MUL Expression %prec LIST_ACCESS',)
    def AssignmentStatement(self, p):
        if self.verbose:
            print("AssignmentStatement", p[0], p[1], p[2])
        return ("AssignmentStatement", p[0], p[1], p[2])

    @_('INT', 'FLOAT')
    def Number(self, p):
        if self.verbose:
            print("Number", p[0])
        return ('Number', p[0])
