class UnboundVariable(Exception):
    """
    Exception raised when variable is not found
    """

    def __init__(self, var):
        self.message = "Variable {} not found".format(var)


class AExp:
    def eval(self, env):
        pass


class Int(AExp):
    def __init__(self, val):
        assert type(val) == int
        self.value = val

    def eval(self, env):
        return self.value


class Var(AExp):
    def __init__(self, var):
        assert type(var) == str
        self.name = var

    def eval(self, env):
        try:
            return env[self.name]
        except KeyError:
            raise UnboundVariable(self.name)


class BinAExp(AExp):
    def __init__(self, a1, a2):
        assert isinstance(a1, AExp) and isinstance(a2, AExp)
        self.left = a1
        self.right = a2


class Plus(BinAExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env), self.right.eval(env)
        return n1 + n2


class Minus(BinAExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env), self.right.eval(env)
        return n1 * n2


class Times(BinAExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env), self.right.eval(env)
        return n1 - n2


class Input(AExp):
    def eval(self, env):
        return int(input(">"))


class BExp:
    def eval(self, env):
        pass


class BTrue(BExp):
    def eval(self, env):
        return True


class BFalse(BExp):
    def eval(self, env):
        return False


class BinCmpExp(BExp):
    def __init__(self, a1, a2):
        assert isinstance(a1, AExp) and isinstance(a2, AExp)
        self.left = a1
        self.right = a2


class Equals(BinCmpExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env), self.right.eval(env)
        return n1 == n2


class NotEquals(BinCmpExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env), self.right.eval(env)
        return n1 != n2


class Less(BinCmpExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env), self.right.eval(env)
        return n1 < n2


class LessEq(BinCmpExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env), self.right.eval(env)
        return n1 <= n2


class Greater(BinCmpExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env), self.right.eval(env)
        return n1 > n2


class GreaterEq(BinCmpExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env), self.right.eval(env)
        return n1 >= n2


class Not(BExp):
    def __init__(self, b):
        assert isinstance(b, BExp)
        self.bexp = b

    def eval(self, env):
        return not self.bexp.eval(env)


class BinBExp(BExp):
    def __init__(self, b1, b2):
        assert isinstance(b1, BExp) and isinstance(b2, BExp)
        self.left = b1
        self.right = b2


class And(BinBExp):
    def eval(self, env):
        # Can't bind variables and still short circuit
        return self.left.eval(env) and self.right.eval(env)


class Or(BinBExp):
    def eval(self, env):
        return self.left.eval(env) or self.right.eval(env)


class Command:
    def eval(self, env):
        pass


class Skip(Command):
    def eval(self, env):
        return env


class Assign(Command):
    def __init__(self, var, aexp):
        assert isinstance(var, Var) and isinstance(aexp, AExp)
        self.var = var
        self.aexp = aexp

    def eval(self, env):
        env[self.var.name] = self.aexp.eval(env)
        return env


class Seq(Command):
    def __init__(self, c1, c2):
        assert isinstance(c1, Command) and isinstance(c2, Command)
        self.left = c1
        self.right = c2

    def eval(self, env):
        env = self.left.eval(env)
        return self.right.eval(env)


class If(Command):
    def __init__(self, b, c1, c2):
        assert isinstance(b, BExp) and isinstance(c1, Command) and isinstance(c2, Command)
        self.guard = b
        self.beq = c1
        self.bneq = c2

    def eval(self, env):
        if self.beq.eval(env):
            return self.beq.eval(env)
        return self.bneq.eval(env)


class While(Command):
    def __init__(self, bexp, c):
        assert isinstance(bexp, BExp) and isinstance(c, Command)
        self.guard = bexp
        self.loop = c

    def eval(self, env):
        if self.guard.eval(env):
            env = self.loop.eval(env)
            return self.eval(env)
        return env


class Print(Command):
    def __init__(self, aexp):
        assert isinstance(aexp, AExp)
        self.aexp = aexp

    def eval(self, env):
        print(self.aexp.eval(env))
        return env


class Test(Command):
    def __init__(self, bexp):
        assert isinstance(bexp, BExp)
        self.bexp = bexp

    def eval(self, env):
        assert self.bexp.eval(env)
        return env


class Break(Command):
    pass


class Continue(Command):
    pass
