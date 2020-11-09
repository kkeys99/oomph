from ply import yacc
import oomphlex

tokens = oomphlex.tokens

# Programs
def p_program(p):
    'p : c EOF'
    pass

# Arithmetic Expressions
def p_aexp(p):
    '''
    a : a PLUS ta
      | a MINUS ta
      | ta
    '''
    pass

def p_ta(p):
    '''
    ta : ta TIMES aa
       | aa
    '''
    pass

def p_aa(p):
    '''
    aa : INT
       | VAR
       | LPAREN a RPAREN
       | INPUT
    '''
    pass

# Boolean Expressions
def p_bexp(p):
    '''
    b : a EQUALS a
      | a NOTEQUALS a
      | a LESS a
      | a LESSEQ a
      | a GREATER a
      | a GREATEREQ a
      | db
    '''
    pass

def p_db(p):
    '''
    db : db OR cb
       | cb
    '''
    pass

def p_cb(p):
    '''
    cb : cb AND nb
       | nb
    '''
    pass

def p_nb(p):
    '''
    nb : NOT ab
       | ab
    '''
    pass

def p_ab(p):
    '''
    ab : TRUE
       | FALSE
       | LPAREN b RPAREN
    '''
    pass

# Commands
def p_command(p):
    '''
    c : ic SEMI c 
      | ic
    '''
    pass

def p_ic(p):
    '''
    ic : IF b THEN ac ELSE ac
       | WHILE b DO ac
       | ac
    '''
    pass

def p_ac(p):
    '''
    ac : SKIP
       | VAR ASSIGN a
       | LBRACE c RBRACE
       | PRINT a
       | TEST b
       | BREAK
       | CONTINUE
    '''
    pass

# Error rule for syntax errors
def p_error(p):
    pass


parser = yacc.yacc()

if __name__ == "__main__":
    with open('input.oomph') as file:
        prog = file.read()
    print(prog)
    result = parser.parse(prog)
    print(result)