from ply import lex

# Reserved words
reserved = (
    'TRUE', 'FALSE', 'NOT', 'AND', 'OR', 'SKIP', 'BREAK', 'CONTINUE', 'IF', 'THEN', 'ELSE', 
    'WHILE', 'DO', 'TEST', 'INPUT', 'PRINT',
)

tokens = reserved + (
    # Literals (variable, integer)
    'VAR', 'INT',

    # Operators (+, -, *, =, !=, <, <=, >, >=)
    'PLUS', 'MINUS', 'TIMES', 'EQUALS', 'NOTEQUALS', 'LESS', 'LESSEQ', 'GREATER', 'GREATEREQ', 

    # Assignment (:=)
    'ASSIGN', 

    # Delimiters ( ) ;
    'SEMI', 'LPAREN', 'RPAREN',

    # End of file
    'EOF',
)

# Completely ignored characters, space and tab
t_ignore           = ' \t'


# Newlines
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_EQUALS           = r'='
t_NOTEQUALS        = r'!='
t_LESS             = r'<'
t_LESSEQ           = r'<='
t_GREATER          = r'>'
t_GREATEREQ        = r'>='

# Assignment
t_ASSIGN           = r':='

# Delimiters
t_SEMI             = r';'
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
# t_LBRACE           = r'\['
# t_RBRACE           = r'\]'

# Variables and reserved words
reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r


def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value,'VAR')
    return t


# End of file
def t_eof(t):
    if not t.lexer.end:
        t.lexer.end = True
        t.type = 'EOF'
        return t


# Integer literals
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
lexer.end = False
if __name__ == "__main__":
    lex.runmain(lexer)
