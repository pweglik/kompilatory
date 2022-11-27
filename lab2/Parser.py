#!/usr/bin/python

from lexer import SimpleLexer
from sly import Parser


scanner_obj = SimpleLexer()

class SimpleParser(Parser):
    tokens = SimpleLexer.tokens
    

    @_('StatementList')
    def Program(self, p):
        print('Program')
        return

    @_('')
    def empty(self, p):
        return

    @_('StatementList Statement',
        'empty')
    def StatementList(self, p):
        return

    @_('CompoundStatement',
        'SelectionStatement',
        'IterationStatement',
        'JumpStatement ";"',
        'PrintStatement ";"',
        'AssignmentStatement ";"',
        'ExpressionStatement')
    def Statement(self, p):
        return

    
    @_('"{" StatementList "}"')
    def CompoundStatement(self, p):
        return

    @_('Expression')
    def ExpressionStatement(self, p):
        return

    @_('IF "(" Expression ")" Statement',
        'IF "(" Expression ")" Statement ELSE Statement')
    def SelectionStatement(self, p):
        return

    @_('WHILE "(" Expression ")" Statement',
        'FOR ID ASS Range Statement',
        'FOR ID ASS List Statement')
    def IterationStatement(self, p):
        return


    @_('BREAK',
        'CONTINUE',
        'RETURN Expression')
    def JumpStatement(self, p):
        return


    @_('PRINT Expression')
    def PrintStatement(self, p):
        return

    @_('Expression ComparisonOperator Expression',
        'Expression BinaryOperator Expression',
        'PrefixUnaryOperator Expression',
        'Expression PostfixUnaryOperator',
        'Matrix',
        'Primitive',
        'ID')
    def Expression(self, p):
        return

    @_('empty',
        '"[" MatrixAccessRange "," MatrixAccessRange "]"')
    def MatrixAccess(self, p):
        return

    @_('MatrixAccessRangeElement ":" MatrixAccessRangeElement',
        'MatrixAccessRangeElement')
    def MatrixAccessRange(self, p):
        return

    @_('INT', 'ID')
    def MatrixAccessRangeElement(self, p):
        return

    @_('RangeElement ":" RangeElement',
        'RangeElement ":" RangeElement ":" RangeElement')
    def Range(self, p):
        return

    @_('Number', 'ID')
    def RangeElement(self, p):
        return

    @_('"[" ListContent "]"')
    def List(self, p):
        return

    @_('ListEl "," ListContent',
        'empty')
    def ListContent(self, p):
        return

    @_('ID', 'Primitive', 'List')
    def ListEl(self, p):
        return

    @_('Number',
        'STRING')
    def Primitive(self, p):
        return

    @_('ZEROS "(" INT ")"',
        'ONES "(" INT ")"',
        'EYE "(" INT ")"',
        '"[" MatrixRowList "]"')
    def Matrix(self, p):
        return

    
    @_('"[" MatrixRow "]" "," MatrixRowList', 'empty', )
    def MatrixRowList(self, p):
        return

    @_('Number "," MatrixRow', 'empty')
    def MatrixRow(self, p):
        return

    @_('ADD', 'SUB', 'MUL', 'DIV', 
    'ADD_EL','SUB_EL', 'MUL_EL', 'DIV_EL')
    def BinaryOperator(self, p):
        return

    @_('ID AssignmentOperator Expression', 
        'ID MatrixAccess AssignmentOperator Expression')
    def AssignmentStatement(self, p):
        return

    @_('ASS', 'ASS_ADD', 'ASS_SUB', 'ASS_DIV', 'ASS_MUL')
    def AssignmentOperator(self, p):
        return

    @_('SUB', 'empty')
    def PrefixUnaryOperator(self, p):
        return

    @_('MAT_TRANS', 'empty')
    def PostfixUnaryOperator(self, p):
        return

    @_('INT', 'FLOAT')
    def Number(self, p):
        return

    @_('EQ', 'LESS_EQ', 'GREATER_EQ', 'NOT_EQ', 'GREATER', 'LESS')
    def ComparisonOperator(self, p):
        return


