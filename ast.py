class UnboundVariable(Exception):
    """
    Exception raised when variable is not found
    """

    def __init__(self, var):
        self.message = "Variable {} not found".format(var)


class NotAFunction(Exception):
    """
    Exception raised when a non function value is applied as a function
    """
    pass


class Closure:
    def __init__(self, expr, args, env):
        assert isinstance(expr, Expr)
        for a in args:
            assert isinstance(a, Var)
        self.expr = expr
        self.args = args
        self.env = env


class Expr:
    def eval(self, env):
        return None, None


class Int(Expr):
    def __init__(self, val):
        assert type(val) == int
        self.value = val

    def eval(self, env):
        return self.value, env


class BTrue(Expr):
    def eval(self, env):
        return True, env


class BFalse(Expr):
    def eval(self, env):
        return False, env


class Var(Expr):
    def __init__(self, var):
        assert type(var) == str
        self.name = var

    def eval(self, env):
        try:
            return env[self.name], env
        except KeyError:
            raise UnboundVariable(self.name)


class Function(Expr):
    def __init__(self, params, exp):
        for p in params:
            assert isinstance(p, Var)
        assert isinstance(exp, Expr)
        self.args = params
        self.exp = exp

    def eval(self, env):
        return Closure(self.exp, self.args, env), env


class App(Expr):
    def __init__(self, func, args):
        assert isinstance(func, Expr)
        for a in args:
            assert isinstance(a, Expr)
        self.func = func
        self.args = args

    def eval(self, env):
        clos, env = self.func.eval(env)
        new_env = {k: v.eval(env)[0] for (k, v) in zip(clos.args, self.args)}
        return clos.eval({**new_env, **env})


class BinExp(Expr):
    def __init__(self, a1, a2):
        assert isinstance(a1, Expr) and isinstance(a2, Expr)
        self.left = a1
        self.right = a2


class Plus(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 + n2, env


class Minus(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 - n2, env


class Times(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 * n2, env


class Input(Expr):
    def eval(self, env):
        return int(input(">")), env


class Equals(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 == n2, env


class NotEquals(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 != n2


class Less(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env[0]), self.right.eval(env)[0]
        return n1 < n2, env


class LessEq(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 <= n2, env


class Greater(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 > n2, env


class GreaterEq(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 >= n2, env


class Not(Expr):
    def __init__(self, b):
        assert isinstance(b, Expr)
        self.bexp = b

    def eval(self, env):
        return not self.bexp.eval(env)[0], env


class And(BinExp):
    def eval(self, env):
        # Can't bind variables and still short circuit
        return self.left.eval(env)[0] and self.right.eval(env)[0], env


class Or(BinExp):
    def eval(self, env):
        return self.left.eval(env)[0] or self.right.eval(env)[0], env


class Unit(Expr):
    def eval(self, env):
        return (), env


class Skip(Expr):
    def eval(self, env):
        return (), env


class Assign(Expr):
    def __init__(self, var, exp):
        assert isinstance(var, Var) and isinstance(exp, Expr)
        self.var = var
        self.exp = exp

    def eval(self, env):
        env[self.var.name] = self.exp.eval(env)[0]
        return (), env


class Seq(Expr):
    def __init__(self, c1, c2):
        assert isinstance(c1, Expr) and isinstance(c2, Expr)
        self.left = c1
        self.right = c2

    def eval(self, env):
        _, env = self.left.eval(env)
        return self.right.eval(env)


class If(Expr):
    def __init__(self, b, c1, c2):
        assert isinstance(b, Expr) and isinstance(c1, Expr) and isinstance(c2, Expr)
        self.guard = b
        self.beq = c1
        self.bneq = c2

    def eval(self, env):
        if self.beq.eval(env)[0]:
            return self.beq.eval(env)
        return self.bneq.eval(env)


class While(Expr):
    def __init__(self, bexp, c):
        assert isinstance(bexp, Expr) and isinstance(c, Expr)
        self.guard = bexp
        self.loop = c

    def eval(self, env):
        if self.guard.eval(env)[0]:
            _, env = self.loop.eval(env)
            return self.eval(env)
        return env


class Print(Expr):
    def __init__(self, exp):
        assert isinstance(exp, Expr)
        self.exp = exp

    def eval(self, env):
        v, env = self.exp.eval(env)
        print(v)
        return v, env


class Test(Expr):
    def __init__(self, exp):
        assert isinstance(exp, Expr)
        self.exp = exp

    def eval(self, env):
        b = self.exp.eval(env)
        assert b[0]
        return b


class Break(Expr):
    pass


class Continue(Expr):
    pass
