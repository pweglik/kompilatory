import unittest
from lexer import *
from typing import List

class TestBasicArythmeticExperssions(unittest.TestCase):

    def setUp(self):
        self.lexer = SimpleLexer()

    def get_return_list(self, text: str):
        token_list = []
        for token in self.lexer.tokenize(text):
            token_list.append(token.type)

        return token_list

    def test_add(self):
        text = """
        +
        """
        self.assertEqual(
            self.get_return_list(text),
            ['ADD']
        )
    
    def test_sub(self):
        text = """
        -
        """
        self.assertEqual(
            self.get_return_list(text),
            ['SUB']
        )

    def test_mul(self):
        text = """
        *
        """
        self.assertEqual(
            self.get_return_list(text),
            ['MUL']
        )

    def test_div(self):
        text = """
        /
        """
        self.assertEqual(
            self.get_return_list(text),
            ['DIV']
        )

    def test_ass(self):
        text = """
        =
        """
        self.assertEqual(
            self.get_return_list(text),
            ['ASS']
        )

    def test_mat_trans(self):
        text = """
        '
        """
        self.assertEqual(
            self.get_return_list(text),
            ['MAT_TRANS']
        )

    def test_ass_add(self):
        text = """
        +=
        """
        self.assertEqual(
            self.get_return_list(text),
            ['ASS_ADD']
        )

    def test_ass_sub(self):
        text = """
        -=
        """
        self.assertEqual(
            self.get_return_list(text),
            ['ASS_SUB']
        )

    def test_ass_mul(self):
        text = """
        *=
        """
        self.assertEqual(
            self.get_return_list(text),
            ['ASS_MUL']
        )

    def test_ass_div(self):
        text = """
        /=
        """
        self.assertEqual(
            self.get_return_list(text),
            ['ASS_DIV']
        )

    def test_add_el(self):
        text = """
        .+
        """
        self.assertEqual(
            self.get_return_list(text),
            ['ADD_EL']
        )

    def test_sub_el(self):
        text = """
        .-
        """
        self.assertEqual(
            self.get_return_list(text),
            ['SUB_EL']
        )

    def test_mul_el(self):
        text = """
        .*
        """
        self.assertEqual(
            self.get_return_list(text),
            ['MUL_EL']
        )

    def test_div_el(self):
        text = """
        ./
        """
        self.assertEqual(
            self.get_return_list(text),
            ['DIV_EL']
        )


    def test_less_eq(self):
        text = """
        >=
        """
        self.assertEqual(
            self.get_return_list(text),
            ['LESS_EQ']
        )

    def test_greater_eq(self):
        text = """
        <=
        """
        self.assertEqual(
            self.get_return_list(text),
            ['GREATER_EQ']
        )

    def test_not_eq(self):
        text = """
        !=
        """
        self.assertEqual(
            self.get_return_list(text),
            ['NOT_EQ']
        )

    def test_eq(self):
        text = """
        ==
        """
        self.assertEqual(
            self.get_return_list(text),
            ['EQ']
        )

    def test_less(self):
        text = """
        <
        """
        self.assertEqual(
            self.get_return_list(text),
            ['LESS']
        )

    def test_greater(self):
        text = """
        >
        """
        self.assertEqual(
            self.get_return_list(text),
            ['GREATER']
        )

    def test_block_starter(self):
        text = """
        :
        """
        self.assertEqual(
            self.get_return_list(text),
            ['BLOCK_STARTER']
        )

    def test_if(self):
        text = """
        if
        """
        self.assertEqual(
            self.get_return_list(text),
            ['IF']
        )

    def test_else(self):
        text = """
        else
        """
        self.assertEqual(
            self.get_return_list(text),
            ['ELSE']
        )

    def test_for(self):
        text = """
        for
        """
        self.assertEqual(
            self.get_return_list(text),
            ['FOR']
        )

    def test_while(self):
        text = """
        while
        """
        self.assertEqual(
            self.get_return_list(text),
            ['WHILE']
        )

    def test_break(self):
        text = """
        break
        """
        self.assertEqual(
            self.get_return_list(text),
            ['BREAK']
        )

    def test_continue(self):
        text = """
        continue
        """
        self.assertEqual(
            self.get_return_list(text),
            ['CONTINUE']
        )

    def test_return(self):
        text = """
        return
        """
        self.assertEqual(
            self.get_return_list(text),
            ['RETURN']
        )

    def test_zeros(self):
        text = """
        zeros
        """
        self.assertEqual(
            self.get_return_list(text),
            ['ZEROS']
        )

    def test_ones(self):
        text = """
        ones
        """
        self.assertEqual(
            self.get_return_list(text),
            ['ONES']
        )

    def test_print(self):
        text = """
        print
        """
        self.assertEqual(
            self.get_return_list(text),
            ['PRINT']
        )

    def test_id(self):
        text = """
        a
        a+
        a+a
        aaa00aa
        _a
        _0
        _a0
        """
        self.assertEqual(
            self.get_return_list(text),
            [
                'ID',
                'ID', 'ADD',
                'ID', 'ADD', 'ID',
                'ID',
                'ID',
                'ID',
                'ID'
            ]
        )

    def test_int(self):
        text = """
        1
        3
        12341234
        0
        53
        """
        self.assertEqual(
            self.get_return_list(text),
            [
                'INT',
                'INT',
                'INT',
                'INT',
                'INT',
            ]
        )

    def test_int_0_before_number(self):
        text = """
            01
        """
        with self.assertRaises(ValueError):
            self.get_return_list(text)

    def test_int_letter(self):
        text = """
            323aa
        """
        with self.assertRaises(ValueError):
            self.get_return_list(text)

    def test_float(self):
        text = """
        1.5
        24124.23213454
        .143
        0.123
        0.123E4
        0.123E-5
        """
        self.assertEqual(
            self.get_return_list(text),
            [
                'FLOAT',
                'FLOAT',
                'FLOAT',
                'FLOAT',
                'FLOAT',
                'FLOAT',
            ]
        )

    def test_float_letter(self):
        text = """
            323.12aaa
        """
        with self.assertRaises(ValueError):
            self.get_return_list(text)

    def test_string(self):
        text = """
            \"string content\"
            \"abvnvneaopibseaASFASF1235152_\"
            \"abcd\"\"01234\"
        """
        self.assertEqual(
            self.get_return_list(text),
            [
                'STRING',
                'STRING',
                'STRING',
                'STRING',
            ]
        )


if __name__ == '__main__':
    unittest.main()
