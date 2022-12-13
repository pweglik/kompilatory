#!/usr/bin/python

from lexer import SimpleLexer
from sly import Parser


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
        return [p[0]]+ p[1]

    @_('Statement')
    def StatementList(self, p):
        if self.verbose:
            print("StatementList", p[0])
        return [p[0]]

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
        if self.verbose:
            print("SelectionStatement", p[2], p[4], p[6])
        return "IF_ELSE_TAG", (("IF", p[2]), ("THEN", p[4]), ("ELSE", p[6]))

    @_('WHILE "(" Expression ")" Statement')
    def IterationStatement(self, p):
        if self.verbose:
            print("IterationStatement", p[0], p[1], p[2], p[3], p[4])
        return 'WHILE', p[2], p[4]

    @_('FOR ID ASS Range Statement',
        'FOR ID ASS List Statement')
    def IterationStatement(self, p):
        if self.verbose:
            print("IterationStatement", p[0], p[1], p[2], p[3], p[4])
        return 'FOR', p[1], p[2], p[4]

    @_('BREAK',
        'CONTINUE')
    def JumpStatement(self, p):
        if self.verbose:
            print("JumpStatement", p[0])
        return p[0].upper()

    @_(
        'RETURN Expression')
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
        return (p[1], p[0], p[2])


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
        return ('-', p[1])


    @_('Expression MAT_TRANS')
    def Expression(self, p):
        if self.verbose:
            print('Expression', p[0], p[1])
        return ('TRANSPOSE', p[0])

    @_('List', 
    'Primitive', 
    'ID', 
    'MatrixFunctions')
    def Expression(self, p):
        if self.verbose:
            print('Expression', p[0])
        return p[0]

    @_('ID ListAccess' )
    def Expression(self, p):
        if self.verbose:
            print('Expression', p[0])
        return p[1], p[0]

    @_('"[" ListAccessElement "]"')
    def ListAccess(self, p):
        if self.verbose:
            print("ListAccess", p[1])
        return ('Access', [p[1]])

    @_('"[" ListAccessElement "]" ListAccess')
    def ListAccess(self, p):
        if self.verbose:
            print("ListAccess", p[1], p[3])
        return ('Access', [p[1]] + p[3][1])

    @_('INT', 'ID')
    def ListAccessElement(self, p):
        if self.verbose:
            print("ListAccessElement", p[0])
        return p[0]

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
        return p[0]

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
    def MatrixFunctions(self, p):
        if self.verbose:
            print("Matrix", p[0], p[2])
        return (p[0], p[2])


    @_('ID ASS Expression',
    'ID ASS_ADD Expression',
    'ID ASS_SUB Expression',
    'ID ASS_DIV Expression',
    'ID ASS_MUL Expression',)
    def AssignmentStatement(self, p):
        if self.verbose:
            print("AssignmentStatement", p[0], p[1], p[2])
        return (p[1], p[0], p[2])


    @_(
    'ID ListAccess ASS Expression', 
    'ID ListAccess ASS_ADD Expression',
    'ID ListAccess ASS_SUB Expression',
    'ID ListAccess ASS_DIV Expression',
    'ID ListAccess ASS_MUL Expression',)
    def AssignmentStatement(self, p):
        if self.verbose:
            print("AssignmentStatement", p[0], p[1], p[2])
        return (p[2], (p[0], p[1]), p[3])


    @_('INT', 'FLOAT')
    def Number(self, p):
        if self.verbose:
            print("Number", p[0])
        return p[0]
