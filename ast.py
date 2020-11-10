class AExp: pass

class Int(AExp):
    def __init__(self, val):
        assert type(val) == int
        self.value = val

class Var(AExp):
    def __init__(self, var):
        assert type(var) == str
        self.name = var

class BinAExp(AExp):
    def __init__(self, a1, a2):
        assert isinstance(a1, AExp) and isinstance(a2, AExp)
        self.left = a1
        self.right = a2

class Plus(BinAExp): pass

class Minus(BinAExp): pass

class Times(BinAExp): pass

class Input(AExp): pass

class BExp: pass

class BTrue(BExp): pass

class BFalse(BExp): pass

class BinCmpExp(BExp):
    def __init__(self, a1, a2):
        assert isinstance(a1, AExp) and isinstance(a2, AExp)
        self.left = a1
        self.right = a2

class Equals(BinCmpExp): pass

class NotEquals(BinCmpExp): pass

class Less(BinCmpExp): pass

class LessEq(BinCmpExp): pass

class Greater(BinCmpExp): pass

class GreaterEq(BinCmpExp): pass

class Not(BExp):
    def __init__(self, b):
        assert isinstance(b, BExp)
        self.bexp = b

class BinBExp(BExp):
    def __init__(self, b1, b2):
        assert isinstance(b1, BExp) and isinstance(b2, BExp)
        self.left = b1
        self.right = b2

class And(BinBExp): pass

class Or(BinBExp): pass

class Command: pass

class Skip(Command): pass

class Assign(Command):
    def __init__(self, var, aexp):
        assert isinstance(var, Var) and isinstance(aexp, AExp)
        self.var = var
        self.aexp = aexp

class Seq(Command):
    def __init__(self, c1, c2):
        assert isinstance(c1, Command) and isinstance(c2, Command)
        self.left = c1
        self.right = c2

class If(Command):
    def __init__(self, b, c1, c2):
        assert isinstance(b, BExp) and isinstance(c1, Command) and isinstance(c2, Command)
        self.guard = b
        self.beq = c1
        self.bneq = c2

class While(Command):
    def __init__(self, bexp, c):
        assert isinstance(bexp, BExp) and isinstance(c, Command)
        self.guard = bexp
        self.loop = c

class Print(Command):
    def __init__(self, aexp):
        assert isinstance(aexp, AExp)
        self.aexp = aexp

class Test(Command):
    def __init__(self, bexp):
        assert isinstance(bexp, BExp)
        self.bexp = bexp

class Break(Command): pass

class Continue(Command): pass