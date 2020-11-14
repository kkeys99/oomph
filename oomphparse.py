from ply import yacc
from ast import *
import oomphlex

tokens = oomphlex.tokens

precedence = (
    ('nonassoc', 'ELSE', 'DO'),
    ('left', 'SEMI'),
    ('nonassoc', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOTEQUALS'),
    ('left', 'LESS', 'LESSEQ', 'GREATER', 'GREATEREQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES'),
    ('right', 'NOT'),
    ('right', 'PRINT', 'TEST'),
    # ('right', 'UMINUS'),            # Unary minus operator
 )


# Programs
def p_program(p):
    'p : c EOF'
    p[0] = p[1]


# Arithmetic Expressions
def p_c_aexp(p):
    '''
    c : c PLUS c
      | c MINUS c
      | c TIMES c
    '''
    if p[2] == '+':
        p[0] = Plus(p[1], p[3])
    elif p[2] == '-':
        p[0] = Minus(p[1], p[3])
    elif p[2] == '*':
        p[0] = Times(p[1], p[3])


def p_c_parens(p):
    '''
    c : LPAREN c RPAREN
    '''
    p[0] = p[2]


def p_c_int(p):
    '''
    c : INT
    '''
    p[0] = Int(p[1])


def p_c_var(p):
    '''
    c : VAR
    '''
    p[0] = Var(p[1])


def p_c_input(p):
    '''
    c : INPUT
    '''
    p[0] = Input()


# Boolean Expressions
def p_c_bexp(p):
    '''
    c : c EQUALS c
      | c NOTEQUALS c
      | c LESS c
      | c LESSEQ c
      | c GREATER c
      | c GREATEREQ c
    '''
    if p[2] == oomphlex.t_EQUALS:
        p[0] = Equals(p[1], p[3])
    elif p[2] == oomphlex.t_NOTEQUALS:
        p[0] = NotEquals(p[1], p[3])
    elif p[2] == oomphlex.t_LESS:
        p[0] = Less(p[1], p[3])
    elif p[0] == oomphlex.t_LESSEQ:
        p[0] = LessEq(p[1], p[3])
    elif p[0] == oomphlex.t_GREATER:
        p[0] = Greater(p[1], p[3])
    elif p[0] == oomphlex.t_GREATEREQ:
        p[0] = GreaterEq(p[1], p[3])


def p_c_binop(p):
    '''
    c : c OR c
       | c AND c
    '''
    if p[2] == 'and':  # This feels wrong... any better way?
        p[0] = And(p[1], p[3])
    elif p[2] == 'and':
        p[0] = Or(p[1], p[3])


def p_c_unop(p):
    '''
    c : NOT c
    '''
    p[0] = Not(p[2])


def p_c_const(p):
    '''
    c : TRUE
       | FALSE
    '''
    if p[1] == oomphlex.reserved_map['TRUE']:
        p[0] = BTrue()
    elif p[1] == oomphlex.reserved_map['FALSE']:
        p[0] = BFalse()


# Commands
def p_c_seq(p):
    '''
    c : c SEMI c
    '''
    p[0] = Seq(p[1], p[3])


def p_c_if(p):
    '''
    c : IF c THEN c ELSE c
    '''
    p[0] = If(p[2], p[4], p[6])


def p_c_while(p):
    '''
    c : WHILE c DO c
    '''
    p[0] = While(p[2], p[4])


def p_c_skip(p):
    '''
    c : SKIP
    | BREAK
    | CONTINUE
    '''
    pass


def p_c_units(p):
    '''
    c : PRINT c
    | TEST c
    '''
    if p[1] == 'print':
        p[0] = Print(p[2])
    elif p[1] == 'test':
        p[0] = Test(p[2])


def p_c_assign(p):
    '''
    c : VAR ASSIGN c
    '''
    p[0] = Assign(Var(p[1]), p[3])


# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

if __name__ == "__main__":
    with open('input.oomph') as file:
        prog = file.read()
    print(prog)
    result = parser.parse(prog)
    print(result)
