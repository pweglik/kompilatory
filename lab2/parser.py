#!/usr/bin/python

from lexer import SimpleLexer
from sly import Parser


scanner_obj = SimpleLexer()

class SimpleParser(Parser):
    tokens = SimpleLexer.tokens
    
    # precedence = (
    #     ('left', ADD, SUB),
    #     ('left', MUL, DIV),
    #     ('right', SUB),
    # )

    @_('StatementList')
    def Program(self, p):
        return ('Program', [l for l in p])

    @_('')
    def empty(self, p):
        print("empty")
        return

    @_('StatementList Statement')
    def StatementList(self, p):
        print("StatementList", p[0], p[1])
        return ("StatementList", p[0], p[1])

    @_('empty')
    def StatementList(self, p):
        print("StatementList")
        return

    @_('CompoundStatement',
        'SelectionStatement',
        'IterationStatement',
        'JumpStatement ";"',
        'PrintStatement ";"',
        'AssignmentStatement ";"',
        'ExpressionStatement ";"')
    def Statement(self, p):
        print("Statement", p[0])
        return ("Statement", p[0])

    
    @_('"{" StatementList "}"')
    def CompoundStatement(self, p):
        print("CompoundStatement")
        return

    @_('Expression')
    def ExpressionStatement(self, p):
        print("ExpressionStatement", p[0])
        return ("ExpressionStatement", p[0])

    @_('IF "(" Expression ")" Statement',
        'IF "(" Expression ")" Statement ELSE Statement')
    def SelectionStatement(self, p):
        print("SelectionStatement")
        return

    @_('WHILE "(" Expression ")" Statement',
        'FOR ID ASS Range Statement',
        'FOR ID ASS List Statement')
    def IterationStatement(self, p):
        print("IterationStatement")
        return


    @_('BREAK',
        'CONTINUE',
        'RETURN Expression')
    def JumpStatement(self, p):
        print("JumpStatement")
        return


    @_('PRINT Expression')
    def PrintStatement(self, p):
        print("PrintStatement")
        return

    @_('PrefixUnaryOperator SimpleExpression PostfixUnaryOperator')
    def Expression(self, p):
        print("Expression",  p[0], p[1], p[2])
        return ("Expression",  p[0], p[1], p[2])

    @_('SimpleExpression PostfixUnaryOperator')
    def Expression(self, p):
        print("Expression",  p[0], p[1])
        return ("Expression",  p[0], p[1])

    @_('PrefixUnaryOperator "(" ComplexExpression ")" PostfixUnaryOperator')
    def Expression(self, p):
        print("Expression", p[0], p[2], p[4])
        return ("Expression",  p[0], p[2], p[4])

    @_('ComplexExpression')
    def Expression(self, p):
        print("Expression", p[0])
        return ("Expression", p[0])

    @_('Expression ComparisonOperator Expression',
        'Expression BinaryOperator Expression')
    def ComplexExpression(self, p):
        print("ComplexExpression", p[0], p[1], p[2])
        return ("ComplexExpression", p[0], p[1], p[2])

    @_('Matrix', 'Primitive', 'ID')
    def SimpleExpression(self, p):
        print('SimpleExpression', p[0])
        return ('SimpleExpression', p[0])

    @_('empty',
        '"[" MatrixAccessRange "," MatrixAccessRange "]"')
    def MatrixAccess(self, p):
        print("MatrixAccess")
        return

    @_('MatrixAccessRangeElement ":" MatrixAccessRangeElement',
        'MatrixAccessRangeElement')
    def MatrixAccessRange(self, p):
        print("MatrixAccessRange")
        return

    @_('INT', 'ID')
    def MatrixAccessRangeElement(self, p):
        print("MatrixAccessRangeElement")
        return

    @_('RangeElement ":" RangeElement',
        'RangeElement ":" RangeElement ":" RangeElement')
    def Range(self, p):
        print("Range")
        return

    @_('Number', 'ID')
    def RangeElement(self, p):
        print("v")
        return

    @_('"[" ListContent "]"')
    def List(self, p):
        print("List")
        return

    @_('ListEl "," ListContent',
        'empty')
    def ListContent(self, p):
        print("ListContent")
        return

    @_('ID', 'Primitive', 'List')
    def ListEl(self, p):
        print("ListEl")
        return

    @_('Number',
        'STRING')
    def Primitive(self, p):
        print("Primitive", p[0])
        return ('Primitive', p[0])

    @_('ZEROS "(" INT ")"',
        'ONES "(" INT ")"',
        'EYE "(" INT ")"',
        '"[" MatrixRowList "]"')
    def Matrix(self, p):
        print("Matrix")
        return

    
    @_('"[" MatrixRow "]" "," MatrixRowList', 'empty', )
    def MatrixRowList(self, p):
        print("MatrixRowList")
        return

    @_('Number "," MatrixRow', 'empty')
    def MatrixRow(self, p):
        print("MatrixRow")
        return

    @_('ADD', 'SUB', 'MUL', 'DIV', 
    'ADD_EL','SUB_EL', 'MUL_EL', 'DIV_EL')
    def BinaryOperator(self, p):
        print("BinaryOperator", p[0])
        return ("BinaryOperator", p[0])

    @_('ID AssignmentOperator Expression')
    def AssignmentStatement(self, p):
        print("AssignmentStatement", p[0], p[1], p[2])
        return ("AssignmentStatement", p[0], p[1], p[2])

    @_('ID MatrixAccess AssignmentOperator Expression')
    def AssignmentStatement(self, p):
        print("AssignmentStatement", p[0], p[1], p[2], p[3])
        return ("AssignmentStatement", p[0], p[1], p[2], p[3])

    @_('ASS', 'ASS_ADD', 'ASS_SUB', 'ASS_DIV', 'ASS_MUL')
    def AssignmentOperator(self, p):
        print("AssignmentOperator", p[0])
        return ("AssignmentOperator", p[0])

    @_('SUB', 'empty')
    def PrefixUnaryOperator(self, p):
        print("PrefixUnaryOperator", p[0])
        return ('PrefixUnaryOperator', p[0])

    @_('MAT_TRANS', 'MatrixAccess', 'empty')
    def PostfixUnaryOperator(self, p):
        print("PostfixUnaryOperator", p[0])
        return ("PostfixUnaryOperator", p[0])

    @_('INT', 'FLOAT')
    def Number(self, p):
        print("Number", p[0])
        return ('Number', p[0])

    @_('EQ', 'LESS_EQ', 'GREATER_EQ', 'NOT_EQ', 'GREATER', 'LESS')
    def ComparisonOperator(self, p):
        print("ComparisonOperator")
        return ('ComparisonOperator', p[0])


