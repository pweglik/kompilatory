#!/usr/bin/python

from lexer import SimpleLexer
from sly import Parser


scanner_obj = SimpleLexer()

class SimpleParser(Parser):
    tokens = SimpleLexer.tokens
    verbose = False
    
    # precedence = (
    #     ('left', ADD, SUB),
    #     ('left', MUL, DIV),
    #     ('right', SUB),
    # )

    @_('StatementList')
    def Program(self, p):
        return ('Program', p[0])

    @_('')
    def empty(self, p):
        if self.verbose:
            print("empty")
        return

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

    @_('IF "(" Expression ")" Statement ELSE Statement')
    def SelectionStatement(self, p):
        if self.verbose:
            print("SelectionStatement", p[2], p[4], p[6])
        return ("SelectionStatement", p[2], p[4], p[6])

    @_('IF "(" Expression ")" Statement')
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


    # @_('PRINT Expression')
    # def PrintStatement(self, p):
    #     if self.verbose:
    #         print("PrintStatement", p[1])
    #     return ("PrintStatement", p[1])


    @_('PRINT ListContent')
    def PrintStatement(self, p):
        if self.verbose:
            print("PrintStatement", p[1])
        return ("PrintStatement", p[1])



    @_('PrefixUnaryOperator SimpleExpression PostfixUnaryOperator')
    def Expression(self, p):
        if self.verbose:
            print("Expression",  p[0], p[1], p[2])
        return ("Expression",  p[0], p[1], p[2])

    @_('SimpleExpression PostfixUnaryOperator')
    def Expression(self, p):
        if self.verbose:
            print("Expression",  p[0], p[1])
        return ("Expression",  p[0], p[1])

    @_('PrefixUnaryOperator "(" ComplexExpression ")" PostfixUnaryOperator')
    def Expression(self, p):
        if self.verbose:
            print("Expression", p[0], p[2], p[4])
        return ("Expression",  p[0], p[2], p[4])

    @_('ComplexExpression')
    def Expression(self, p):
        if self.verbose:
            print("Expression", p[0])
        return ("Expression", p[0])

    @_('Expression ComparisonOperator Expression',
        'Expression BinaryOperator Expression')
    def ComplexExpression(self, p):
        if self.verbose:
            print("ComplexExpression", p[0], p[1], p[2])
        return ("ComplexExpression", p[0], p[1], p[2])

    #'Matrix'
    @_('MatrixRowList', 'Primitive', 'ID')
    def SimpleExpression(self, p):
        if self.verbose:
            print('SimpleExpression', p[0])
        return ('SimpleExpression', p[0])

    @_('"[" MatrixAccessRange "," MatrixAccessRange "]"')
    def MatrixAccess(self, p):
        if self.verbose:
            print("MatrixAccess", p[1], p[3])
        return ("MatrixAccess", p[1], p[3])

    @_('MatrixAccessRangeElement ":" MatrixAccessRangeElement')
    def MatrixAccessRange(self, p):
        if self.verbose:
            print("MatrixAccessRange", p[0], p[2])
        return ("MatrixAccessRange", p[0], p[2])

    @_('MatrixAccessRangeElement')
    def MatrixAccessRange(self, p):
        if self.verbose:
            print("MatrixAccessRange", p[0])
        return ("MatrixAccessRange", p[0])

    @_('INT', 'ID')
    def MatrixAccessRangeElement(self, p):
        if self.verbose:
            print("MatrixAccessRangeElement", p[0])
        return ("MatrixAccessRangeElement", p[0])

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
    def Matrix(self, p):
        if self.verbose:
            print("Matrix", p[0], p[2])
        return ("Matrix", p[0], p[2])

    @_('"[" MatrixRowList "]"')
    def Matrix(self, p):
        if self.verbose:
            print("Matrix", p[1])
        return ("Matrix", p[1])

    @_('"[" MatrixRow "]" "," MatrixRowList')
    def MatrixRowList(self, p):
        if self.verbose:
            print("MatrixRowList", p[1], p[3])
        return ("MatrixRowList", p[1], p[3])

    @_('"[" MatrixRow "]"')
    def MatrixRowList(self, p):
        if self.verbose:
            print("MatrixRowList", p[1])
        return ("MatrixRowList", p[1])

    @_('Number "," MatrixRow')
    def MatrixRow(self, p):
        if self.verbose:
            print("MatrixRow", p[0], p[1])

        return ("MatrixRow", p[0], p[1])

    @_('Number')
    def MatrixRow(self, p):
        if self.verbose:
            print("MatrixRow", p[0])

        return ("MatrixRow", p[0])

    @_('ADD', 'SUB', 'MUL', 'DIV', 
    'ADD_EL','SUB_EL', 'MUL_EL', 'DIV_EL')
    def BinaryOperator(self, p):
        if self.verbose:
            print("BinaryOperator", p[0])
        return ("BinaryOperator", p[0])

    @_('ID AssignmentOperator Expression')
    def AssignmentStatement(self, p):
        if self.verbose:
            print("AssignmentStatement", p[0], p[1], p[2])
        return ("AssignmentStatement", p[0], p[1], p[2])

    @_('ID MatrixAccess AssignmentOperator Expression')
    def AssignmentStatement(self, p):
        if self.verbose:
            print("AssignmentStatement", p[0], p[1], p[2], p[3])
        return ("AssignmentStatement", p[0], p[1], p[2], p[3])

    @_('ASS', 'ASS_ADD', 'ASS_SUB', 'ASS_DIV', 'ASS_MUL')
    def AssignmentOperator(self, p):
        if self.verbose:
            print("AssignmentOperator", p[0])
        return ("AssignmentOperator", p[0])

    @_('SUB', 'empty')
    def PrefixUnaryOperator(self, p):
        if self.verbose:
            print("PrefixUnaryOperator", p[0])
        return ('PrefixUnaryOperator', p[0])

    @_('MAT_TRANS', 'MatrixAccess', 'empty')
    def PostfixUnaryOperator(self, p):
        if self.verbose:
            print("PostfixUnaryOperator", p[0])
        return ("PostfixUnaryOperator", p[0])

    @_('INT', 'FLOAT')
    def Number(self, p):
        if self.verbose:
            print("Number", p[0])
        return ('Number', p[0])

    @_('EQ', 'LESS_EQ', 'GREATER_EQ', 'NOT_EQ', 'GREATER', 'LESS')
    def ComparisonOperator(self, p):
        if self.verbose:
            print("ComparisonOperator", p[0])
        return ('ComparisonOperator', p[0])


