#!/usr/bin/python

from lexer import SimpleLexer
from sly import Parser


scanner_obj = SimpleLexer()

class SimpleParser(Parser):
    tokens = SimpleLexer.tokens
    

    @_('StatementList')
    def Program(self, p):
        print('Program')
        return p

    @_('')
    def empty(self, p):
        print('empty')
        return p

    @_('StatementList Statement',
        'empty')
    def StatementList(self, p):
        return p

    @_('CompoundStatement',
        'SelectionStatement',
        'IterationStatement',
        'JumpStatement ";"',
        'PrintStatement ";"',
        'AssignmentStatement ";"',
        'ExpressionStatement ;')
    def Statement(self, p):
        return p

    
    @_('"{" StatementList "}"')
    def CompoundStatement(self, p):
        return p

    @_('Expression')
    def ExpressionStatement(self, p):
        print('Expression')
        return p

    @_('IF "(" Expression ")" Statement',
        'IF "(" Expression ")" Statement ELSE Statement')
    def SelectionStatement(self, p):
        return p

    @_('WHILE "(" Expression ")" Statement',
        'FOR ID ASS Range Statement',
        'FOR ID ASS List Statement')
    def IterationStatement(self, p):
        return p


    @_('BREAK',
        'CONTINUE',
        'return p Expression')
    def JumpStatement(self, p):
        return p


    @_('PRINT Expression')
    def PrintStatement(self, p):
        return p

    @_('Expression ComparisonOperator Expression',
        'Expression BinaryOperator Expression',
        'PrefixUnaryOperator Expression',
        'Expression PostfixUnaryOperator',
        'Matrix',
        'Primitive',
        '"(" Expression ")"',
        'ID')
    def Expression(self, p):
        print('ExpressionStatement')
        return p

    @_('empty',
        '"[" MatrixAccessRange "," MatrixAccessRange "]"')
    def MatrixAccess(self, p):
        return p

    @_('MatrixAccessRangeElement ":" MatrixAccessRangeElement',
        'MatrixAccessRangeElement')
    def MatrixAccessRange(self, p):
        return p

    @_('INT', 'ID')
    def MatrixAccessRangeElement(self, p):
        return p

    @_('RangeElement ":" RangeElement',
        'RangeElement ":" RangeElement ":" RangeElement')
    def Range(self, p):
        return p

    @_('Number', 'ID')
    def RangeElement(self, p):
        return p

    @_('"[" ListContent "]"')
    def List(self, p):
        return p

    @_('ListEl "," ListContent',
        'empty')
    def ListContent(self, p):
        return p

    @_('ID', 'Primitive', 'List')
    def ListEl(self, p):
        return p

    @_('Number',
        'STRING')
    def Primitive(self, p):
        return p

    @_('ZEROS "(" INT ")"',
        'ONES "(" INT ")"',
        'EYE "(" INT ")"',
        '"[" MatrixRowList "]"')
    def Matrix(self, p):
        return p

    
    @_('"[" MatrixRow "]" "," MatrixRowList', 'empty', )
    def MatrixRowList(self, p):
        return p

    @_('Number "," MatrixRow', 'empty')
    def MatrixRow(self, p):
        return p

    @_('ADD', 'SUB', 'MUL', 'DIV', 
    'ADD_EL','SUB_EL', 'MUL_EL', 'DIV_EL')
    def BinaryOperator(self, p):
        return p

    @_('ID AssignmentOperator Expression', 
        'ID MatrixAccess AssignmentOperator Expression')
    def AssignmentStatement(self, p):
        return p

    @_('ASS', 'ASS_ADD', 'ASS_SUB', 'ASS_DIV', 'ASS_MUL')
    def AssignmentOperator(self, p):
        return p

    @_('SUB', 'empty')
    def PrefixUnaryOperator(self, p):
        return p

    @_('MAT_TRANS', 'empty')
    def PostfixUnaryOperator(self, p):
        return p

    @_('INT', 'FLOAT')
    def Number(self, p):
        return p

    @_('EQ', 'LESS_EQ', 'GREATER_EQ', 'NOT_EQ', 'GREATER', 'LESS')
    def ComparisonOperator(self, p):
        return p


