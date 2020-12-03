from ply import yacc
from ast import *
import oomphlex

tokens = oomphlex.tokens

precedence = (
    ('left', 'SEMI'),
    ('right', 'COLON'),
    ('nonassoc', 'ASSIGN'),
    ('nonassoc', 'LPAREN', 'RPAREN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOTEQUALS'),
    ('left', 'LESS', 'LESSEQ', 'GREATER', 'GREATEREQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES'),
    ('right', 'NOT'),
    ('right', 'PRINT', 'TEST'),
    ('right', 'DOT')
 )


# Programs
def p_program(p):
    'p : c'
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


def p_vars_fun(p):
    '''
    vars : VAR
         | VAR COMMA vars
    '''
    if len(p) == 2:
        p[0] = [Var(p[1])]
    else:
        p[0] = [Var(p[1])] + p[3]


def p_c_func(p):
    '''
    c : DEF VAR LPAREN vars RPAREN COLON LCURL c RCURL
    '''
    p[0] = Function(Var(p[2]), p[4], p[8])


def p_c_class(p):
    '''
    c : CLASS VAR COLON LCURL c RCURL
    '''
    p[0] = Class(Var(p[2]), p[5])

def p_c_dot(p):
    '''
    c : c DOT c
    '''
    p[0] = Dot(p[1], p[3])

def p_exps_fun(p):
    '''
    exps : c
         | c COMMA exps
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_c_int(p):
    '''
    c : INT
      | MINUS INT
    '''
    if type(p[1]) == str:
        p[0] = Int(-p[2])
    else:
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
    elif p[2] == oomphlex.t_LESSEQ:
        p[0] = LessEq(p[1], p[3])
    elif p[2] == oomphlex.t_GREATER:
        p[0] = Greater(p[1], p[3])
    elif p[2] == oomphlex.t_GREATEREQ:
        p[0] = GreaterEq(p[1], p[3])


def p_c_binop(p):
    '''
    c : c OR c
       | c AND c
    '''
    if p[2] == 'and':  # This feels wrong... any better way?
        p[0] = And(p[1], p[3])
    elif p[2] == 'or':
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
    if p[1] == 'true':
        p[0] = BTrue()
    elif p[1] == 'false':
        p[0] = BFalse()


def p_c_app(p):
    '''
    c : c LPAREN exps RPAREN
    '''
    p[0] = App(p[1], p[3])


# Commands
def p_c_seq(p):
    '''
    c : c SEMI c
    '''
    p[0] = Seq(p[1], p[3])


def p_c_if(p):
    '''
    c : IF LPAREN c RPAREN LCURL c RCURL ELSE LCURL c RCURL
    '''
    p[0] = If(p[3], p[6], p[10])


def p_c_while(p):
    '''
    c : WHILE LPAREN c RPAREN LCURL c RCURL
    '''
    p[0] = While(p[3], p[6])


def p_c_skip(p):
    '''
    c : SKIP
    | BREAK
    | CONTINUE
    '''
    p[0] = Skip()


def p_c_units(p):
    '''
    c : PRINT LPAREN c RPAREN
    | TEST LPAREN c RPAREN
    '''
    if p[1] == 'print':
        p[0] = Print(p[3])
    elif p[1] == 'test':
        p[0] = Test(p[3])


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
