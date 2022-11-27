from sly import Lexer

class SimpleLexer(Lexer):

    tokens = { 
        ADD,
        SUB,
        MUL,
        DIV,
        ADD_EL,
        SUB_EL,
        MUL_EL,
        DIV_EL,
        ASS,
        ASS_ADD,
        ASS_SUB,
        ASS_MUL,
        ASS_DIV,
        LESS,
        GREATER,
        LESS_EQ,
        GREATER_EQ,
        NOT_EQ,
        EQ,
        MAT_TRANS,
        IF,
        ELSE,
        FOR,
        WHILE,
        BREAK,
        CONTINUE,
        RETURN,
        EYE,
        ZEROS,
        ONES,
        PRINT,
        ID,
        INT,
        FLOAT,
        STRING,
    }

    literals = { '(', ')', '[', ']', '{', '}', ',', ':', ';' }

    # Regular expression rules for tokens
    ASS_ADD         = r'\+\='
    ASS_SUB         = r'\-\='
    ASS_MUL         = r'\*\='
    ASS_DIV         = r'\/\='
    ADD_EL          = r'\.\+'
    SUB_EL          = r'\.\-'
    MUL_EL          = r'\.\*'
    DIV_EL          = r'\.\/'
    LESS_EQ         = r'\>\='
    GREATER_EQ      = r'\<\='
    NOT_EQ          = r'\!\='
    EQ              = r'\=\='
    LESS            = r'\<'
    GREATER         = r'\>'
    ADD             = r'\+'
    SUB             = r'\-'
    MUL             = r'\*'
    DIV             = r'\/'
    ASS             = r'\='
    MAT_TRANS       = r'\''

    IF              = r'if'
    ELSE            = r'else'
    FOR             = r'for'
    WHILE           = r'while'
    BREAK           = r'break'
    CONTINUE        = r'continue'
    RETURN          = r'return'
    EYE             = r'eye'
    ZEROS           = r'zeros'
    ONES            = r'ones'
    PRINT           = r'print'

    @_(r'0[1-9][0-9]*')
    def zero_before_number(self, token):
        raise ValueError(f"Illegal number (E1): '{token.value}'!")

    @_(r'(([0-9]+)|((([1-9][0-9]*)|0)?\.[0-9]*(E-?[1-9][0-9]*)?))[a-zA-DF-Z_]')
    def letters_after_number(self, token):
        raise ValueError(f"Illegal number (E2): '{token.value}'!")


    FLOAT           = r'(([1-9][0-9]*)|0)?\.[0-9]*(E-?[1-9][0-9]*)?'
    INT             = r'([1-9][0-9]*)|0'
    ID              = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING          = r'"(([^"\\])|(\\.))*"'

    ignore = ' \t'
    ignore_comment = r'\#.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def find_column(self, text: str, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column

    # Error handling rule
    def error(self, token):
        raise ValueError(f"illegal token: {token}")
