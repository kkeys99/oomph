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

class ClassInfo:
    def __init__(self, classVars, methods):
        """
        Parameter classVars: a list of Var objects
        Parameter methods: a list of Function objects
        """
        assert isinstance(classVars, dict), "Invalid class variable"
        assert isinstance(methods, dict), "Invalid method declaration"
        self.classVars = classVars
        self.methods = methods

    def __getitem__(self, key):
        """
        Note that methods will shadow class variables because of this
        """
        if key in self.methods:
            return self.methods[key]
        if key in self.classVars:
            return self.classVars[key]
        raise AttributeError(key)
        
class Expr:
    def eval(self, env):
        """
        The configuration returned by eval is a tuple with elements

        (value, variableBindings)

        Where value is the value computed by the function
        and variableBindings is a dictionary mapping variable names to their values
        """
        return None, None


class Int(Expr):
    def __init__(self, val):
        assert type(val) == int
        self.value = val

    def eval(self, env):
        return self.value, env

    def __str__(self):
        return str(self.value)


class BTrue(Expr):
    def eval(self, env):
        return True, env

    def __str__(self):
        return "true"


class BFalse(Expr):
    def eval(self, env):
        return False, env

    def __str__(self):
        return "true"


class Var(Expr):
    def __init__(self, var):
        assert type(var) == str, f"{var} is not a variable"
        self.name = var

    def eval(self, env):
        try:
            return env[self.name], env
        except KeyError:
            raise UnboundVariable(self.name)

    def __str__(self):
        return str(self.name)

class Class(Expr):
    def __init__(self, name, body):
        assert isinstance(name, Var), "Class name is invalid"
        assert self.bodyIsOk(body), "Class body can only contain method and variable declarations"
        self.name = name
        self.body = body

    def bodyIsOk(self, body):
        """
        Returns whether body is a sequence of assignment statements and functions 
        (or alternatively just a single statement of those types)
        """
        if isinstance(body, Assign) or isinstance(body, Function):
            return True
        if not isinstance(body, Seq):
            return False
        return self.bodyIsOk(body.left) and self.bodyIsOk(body.right)

    def destructBody(self, body):
        """
        Returns a pair containing (classVars, methods)

        Where classVars is a dictionary mapping variable names to values
        and methods is a dictionary mapping method names to closures

        Parameter body: the body of the class
        """
        if isinstance(body, Assign):
            # Evaluate the assignment statement to get its environment
            _, env = body.eval({})
            return (env, {})
        if isinstance(body, Function):
            # Evaluate the function to get the environment mapping func name to closure
            _, env = body.eval({})
            return ({}, env)
        leftClassVars, leftMethods = self.destructBody(body.left)
        rightClassVars, rightMethods = self.destructBody(body.right)
        return ({**leftClassVars, **rightClassVars}, {**leftMethods, **rightMethods})

    def eval(self, env):
        classInfo = ClassInfo(*self.destructBody(self.body))
        env[self.name.name] = classInfo
        return classInfo, env


class Dot(Expr):
    def __init__(self, obj, attr):
        assert isinstance(obj, Expr), "Left side of a dot operator must be an expression"
        assert isinstance(attr, Var), "Right side of a dot operator must be a variable"
        self.obj = obj
        self.attr = attr

    def eval(self, env):
        attr = self.attr.name
        classInfo, newEnv = self.obj.eval(env)
        return classInfo[attr], newEnv

class Function(Expr):
    def __init__(self, name, params, exp):
        for p in params:
            assert isinstance(p, Var)
        assert isinstance(name, Var)
        assert isinstance(exp, Expr)
        self.name = name
        self.args = params
        self.exp = exp

    def eval(self, env):
        clos = Closure(self.exp, self.args, env.copy())
        clos.env[self.name.name] = clos
        env[self.name.name] = clos
        return clos, env

    def __str__(self):
        args = ",".join(map(str, self.args))
        return f"def {self.name}({args}): {self.exp}"


class App(Expr):
    def __init__(self, func, args):
        assert isinstance(func, Expr)
        for a in args:
            assert isinstance(a, Expr)
        self.func = func
        self.args = args

    def eval(self, env):
        clos, env1 = self.func.eval(env)
        env2 = {k.name: v.eval(env)[0] for (k, v) in zip(clos.args, self.args)}
        return clos.expr.eval({**env2, **clos.env})[0], env1

    def __str__(self):
        args = ",".join(map(str, self.args))
        return f"app {self.func} to ({args})"


class BinExp(Expr):
    def __init__(self, a1, a2):
        assert isinstance(a1, Expr) and isinstance(a2, Expr)
        self.left = a1
        self.right = a2


class Plus(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 + n2, env

    def __str__(self):
        return f"{self.left} + {self.right}"


class Minus(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 - n2, env

    def __str__(self):
        return f"{self.left} - {self.right}"


class Times(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 * n2, env

    def __str__(self):
        return f"{self.left} * {self.right}"


class Input(Expr):
    def eval(self, env):
        return int(input(">")), env

    def __str__(self):
        return "input"


class Equals(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 == n2, env

    def __str__(self):
        return f"{self.left} = {self.right}"


class NotEquals(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 != n2, env

    def __str__(self):
        return f"{self.left} != {self.right}"


class Less(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 < n2, env

    def __str__(self):
        return f"{self.left} < {self.right}"


class LessEq(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 <= n2, env

    def __str__(self):
        return f"{self.left} <= {self.right}"


class Greater(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 > n2, env

    def __str__(self):
        return f"{self.left} > {self.right}"


class GreaterEq(BinExp):
    def eval(self, env):
        n1, n2 = self.left.eval(env)[0], self.right.eval(env)[0]
        return n1 >= n2, env

    def __str__(self):
        return f"{self.left} >= {self.right}"


class Not(Expr):
    def __init__(self, b):
        assert isinstance(b, Expr)
        self.bexp = b

    def eval(self, env):
        return not self.bexp.eval(env)[0], env

    def __str__(self):
        return f"not {self.bexp}"


class And(BinExp):
    def eval(self, env):
        # Can't bind variables and still short circuit
        return self.left.eval(env)[0] and self.right.eval(env)[0], env

    def __str__(self):
        return f"{self.left} and {self.right}"


class Or(BinExp):
    def eval(self, env):
        return self.left.eval(env)[0] or self.right.eval(env)[0], env

    def __str__(self):
        return f"{self.left} or {self.right}"


class Unit(Expr):
    def eval(self, env):
        return (), env

    def __str__(self):
        return "unit"


class Skip(Expr):
    def eval(self, env):
        return (), env

    def __str__(self):
        return "skip"


class Assign(Expr):
    def __init__(self, var, exp):
        assert isinstance(var, Var) and isinstance(exp, Expr)
        self.var = var
        self.exp = exp

    def eval(self, env):
        env[self.var.name] = self.exp.eval(env)[0]
        return (), env

    def __str__(self):
        return f"{self.var} := {self.exp}"


class Seq(Expr):
    def __init__(self, c1, c2):
        assert isinstance(c1, Expr), f"First command {c1} of sequence is not a valid expression!"
        assert isinstance(c2, Expr), f"Second command {c2} of sequence is not a valid expression!"
        self.left = c1
        self.right = c2

    def eval(self, env):
        _, env = self.left.eval(env)
        return self.right.eval(env)

    def __str__(self):
        return f"{self.left} ; {self.right}"


class If(Expr):
    def __init__(self, b, c1, c2):
        assert isinstance(b, Expr) and isinstance(c1, Expr) and isinstance(c2, Expr)
        self.guard = b
        self.beq = c1
        self.bneq = c2

    def eval(self, env):
        if self.guard.eval(env)[0]:
            return self.beq.eval(env)
        return self.bneq.eval(env)

    def __str__(self):
        return f"if {self.guard} then {self.beq} else {self.bneq}"


class While(Expr):
    def __init__(self, bexp, c):
        assert isinstance(bexp, Expr), f'Loop guard {bexp} is not a valid expression!'
        assert isinstance(c, Expr), f'Loop body {c} is not a valid expression!'
        self.guard = bexp
        self.loop = c

    def eval(self, env):
        if self.guard.eval(env)[0]:
            _, env = self.loop.eval(env)
            return self.eval(env)
        return (), env


class Print(Expr):
    def __init__(self, exp):
        assert isinstance(exp, Expr)
        self.exp = exp

    def eval(self, env):
        v, env = self.exp.eval(env)
        print(v)
        return v, env

    def __str__(self):
        return f"print({self.exp})"


class Test(Expr):
    def __init__(self, exp):
        assert isinstance(exp, Expr)
        self.exp = exp

    def eval(self, env):
        b = self.exp.eval(env)
        assert b[0], f'Test expression {b} evaluated to false!'
        return (), env

    def __str__(self):
        return f"test({self.exp})"


class Break(Expr):
    pass


class Continue(Expr):
    pass
