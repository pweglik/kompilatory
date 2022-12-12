#!/usr/bin/python

from lexer import SimpleLexer
from sly import Parser


scanner_obj = SimpleLexer()

class SimpleParser(Parser):
    tokens = SimpleLexer.tokens
    verbose = False
    debugfile='debug.log'
    

    precedence = (
        ('nonassoc', EQ, LESS_EQ, GREATER_EQ, NOT_EQ, GREATER, LESS, IF_PREC),
        ('nonassoc', IF_ELSE_PREC),
        ('left', ADD, SUB),
        ('left', MUL, DIV),
        ('right', UMINUS),
        ('left', LIST_ACCESS, MAT_TRANS),
    )

    @_('StatementList')
    def Program(self, p):
        return ('Program', p[0])

    # @_('')
    # def empty(self, p):
    #     if self.verbose:
    #         print("empty")
    #     return

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
        'ExpressionStatement ";"')
    def Statement(self, p):
        if self.verbose:
            print("Statement", p[0])
        return ("Statement", p[0])

    
    @_('"{" StatementList "}"')
    def CompoundStatement(self, p):
        if self.verbose:
            print("CompoundStatement", p[1])
        return ("CompoundStatement", p[1])

    @_('Expression')
    def ExpressionStatement(self, p):
        if self.verbose:
            print("ExpressionStatement", p[0])
        return ("ExpressionStatement", p[0])

    @_('IF "(" Expression ")" Statement ELSE Statement %prec IF_ELSE_PREC')
    def SelectionStatement(self, p):
        if self.verbose:
            print("SelectionStatement", p[2], p[4], p[6])
        return ("SelectionStatement", p[2], p[4], p[6])

    @_('IF "(" Expression ")" Statement %prec IF_PREC')
    def SelectionStatement(self, p):
        if self.verbose:
            print("SelectionStatement", p[2], p[4])
        return ("SelectionStatement", p[2], p[4])


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
        'Expression ListAccess %prec LIST_ACCESS'
        )
    def Expression(self, p):
        if self.verbose:
            print('Expression', p[0], p[1])
        return ('Expression', p[0], p[1])


    @_('List', 'Primitive', 'ID', 'MatrixFunctions')
    def Expression(self, p):
        if self.verbose:
            print('Expression', p[0])
        return ('Expression', p[0])

    @_('"[" ListAccessContent "]"')
    def ListAccess(self, p):
        if self.verbose:
            print("ListAccess", p[1])
        return ("ListAccess", p[1])

    @_('ListAccessElement')
    def ListAccessContent(self, p):
        if self.verbose:
            print("ListAccessContent", p[0])
        return ("ListAccessContent", p[0])

    @_('ListAccessElement "," ListAccessContent')
    def ListAccessContent(self, p):
        if self.verbose:
            print("ListAccessContent", p[0], p[2])
        return ("ListAccessContent", p[0], p[2])

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

    @_('ListEl "," ListContent')
    def ListContent(self, p):
        if self.verbose:
            print("ListContent", p[0], p[2])
        return ("ListContent", p[0], p[2])

    @_('ListEl')
    def ListContent(self, p):
        if self.verbose:
            print("ListContent", p[0])
        return ("ListContent", p[0])

    @_('Expression', 'List')
    def ListEl(self, p):
        if self.verbose:
            print("ListEl", p[0])
        return ("ListEl", p[0])

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
    'ID ASS_MUL Expression',)
    def AssignmentStatement(self, p):
        if self.verbose:
            print("AssignmentStatement", p[0], p[1], p[2])
        return ("AssignmentStatement", p[0], p[1], p[2])

    @_('INT', 'FLOAT')
    def Number(self, p):
        if self.verbose:
            print("Number", p[0])
        return ('Number', p[0])
