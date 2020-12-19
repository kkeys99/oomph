from enum import Enum


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
    def __init__(self, exp):
        self.message = f"Application of a non function: {exp}"


class Closure:
    def __init__(self, expr, args, env):
        assert isinstance(expr, Expr)
        for a in args:
            assert isinstance(a, Var)
        self.expr = expr
        self.args = args
        self.env = env

    def methodify(self, obj):
        """
        Creates a method version of this closure

        Parameter obj: the object that the method is being called on
        """
        return MethodClosure(self.expr, self.args, self.env, obj, obj.superClass)

    def __str__(self):
        return f"[| {list(map(str, self.args))}, {self.expr}, {self.env}|]"


class MethodClosure(Closure):
    def __init__(self, expr, args, env, obj, superClass):
        super().__init__(expr, args, env)
        self.obj = obj
        self.superClass = superClass


class ClassInfo:
    def __init__(self, name, classVars, methods, superClass):
        """
        Parameter name: the name of this class (a string)
        Parameter classVars: a dictionary mapping variable names to values
        Parameter methods: a dictionary mapping method names to their closures
        Parameter superClass: a string, the name of the superclass of this class, None if there is no superclass
        """
        assert type(name) == str, "Class name must be a string"
        assert isinstance(classVars, dict), "Invalid class variable"
        assert isinstance(methods, dict), "Invalid method declaration"
        assert superClass is None or isinstance(superClass, ClassInfo), "Invalid superclass name"
        self.name = name
        self.classVars = classVars
        self.methods = methods
        self.constructor = methods.get("constructor", None)
        self.superClass = superClass

    def __getitem__(self, key):
        """
        Note that methods will shadow class variables because of this
        """
        if key in self.methods:
            return self.methods[key], AttrOwner.THIS
        if key in self.classVars:
            return self.classVars[key], AttrOwner.THIS
        if self.superClass is not None:
            (val, access), owner = self.superClass[key]
            if access == PrivacyMod.PRIVATE:
                raise TypeError("Subclass can not access private fields of superclass!")
            return (val, access), AttrOwner.SUPER
        raise AttributeError(key)

    def get_owned(self, key, owner):
        if key in self.methods:
            return self.methods[key]
        if key in self.classVars:
            return self.classVars[key]
        if self.superClass is not None:
            val, access = self.superClass[key]
            if access == PrivacyMod.PRIVATE and owner != AttrOwner.SUPER:
                raise TypeError("Subclass can not access private fields of superclass!")
            return val, access
        raise AttributeError(key)

    def __setitem__(self, key, value):
        self.classVars[key] = value

    def __call__(self, args, env):
        return Object(self.name, self.classVars, self.methods, args, self.superClass, env)


class Object(ClassInfo):
    def __init__(self, name, classVars, methods, args, superClass, env):
        super().__init__(name, classVars, methods, superClass)
        self.args = args  # store to make PrivateObject
        self.attributes = {}
        if self.constructor:
            # Insert self for "this" in constructor call
            args.insert(0, self)
            constructor = self.constructor[0] if type(self.constructor) == tuple else self.constructor
            if len(constructor.args) != len(args):
                raise TypeError("Invalid number of arguments for constructor call")
            env2 = {k.name: v.eval(env)[0] for (k, v) in zip(constructor.args, args)}
            env2['this'] = PrivateObject(env2['this'])
            # Bind super to a pair, this and the superclass
            _, newEnv = constructor.expr.eval({**env2, **env, 'super': (self, superClass)})
            self.attributes = newEnv['this'].attributes
        elif len(args) > 0:
            raise TypeError("Constructor takes no arguments")

    def __getitem__(self, key):
        if key in self.attributes:
            return self.attributes[key]
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def eval(self, env):
        return self, env


class PrivateObject:
    """
    Class to represent objects with private access
    """
    def __init__(self, obj):
        assert isinstance(obj, Object), "From_object expects an object"
        self.obj = obj
        self.attributes = obj.attributes
        self.superClass = obj.superClass

    def __getitem__(self, key):
        return self.obj.__getitem__(key)

    def __setitem__(self, key, value):
        self.obj.__setitem__(key, value)

    def eval(self, env):
        return self.obj.eval(env)

    def __call__(self, args):
        return self.obj.__call__(args)


class PrivacyMod(Enum):
    PRIVATE = 1
    PUBLIC = 2
    PROTECTED = 3


class AccessMod(Enum):
    STATIC = 1
    NONSTATIC = 2


class AttrOwner(Enum):
    SUPER = 1
    THIS = 2
    SUB = 3  # Do we need?


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

    def __eq__(self, other):
        if not isinstance(other, Int):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

class List(Expr):
    def __init__(self, val):
        assert type(val) == list
        self.value = val

    def eval(self, env):
        return [elt.eval(env)[0] for elt in self.value], env

    def __eq__(self, other):
        if not isinstance(other, List):
            return False
        return all([a == b for a, b in zip(self.value, other.value)])


class Tuple(Expr):
    def __init__(self, val):
        assert type(val) == tuple
        self.value = val

    def eval(self, env):
        return tuple(elt.eval(env)[0] for elt in self.value), env

    def __eq__(self, other):
        if not isinstance(other, List):
            return False
        return all([a == b for a, b in zip(self.value, other.value)])

    def __hash__(self):
        return hash(self.value)

class Dict(Expr):
    def __init__(self, keyvals):
        self.keyvals = keyvals

    def eval(self, env):
        return {k.eval(env)[0] : v.eval(env)[0] for k, v in self.keyvals}, env

class String(Expr):
    def __init__(self, val):
        assert type(val) == str
        self.value = val

    def eval(self, env):
        return self.value, env
    
    def __str__(self):
        return self.value

    def __eq__(self, other):
        if not isinstance(other, String):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Index(Expr):
    def __init__(self, obj, ind):
        assert isinstance(obj, Expr)
        assert isinstance(ind, Expr)
        self.obj = obj
        self.ind = ind

    def eval(self, env):
        obj, _ = self.obj.eval(env)
        ind, _ = self.ind.eval(env)
        assert type(obj) in [str, list, tuple, dict], 'Can only index a string or list'
        return obj[ind], env


class Slice(Expr):
    def __init__(self, obj, start, end):
        assert isinstance(obj, Expr)
        assert isinstance(start, Expr) or start is None
        assert isinstance(end, Expr) or end is None
        self.obj = obj
        self.start = start
        self.end = end

    def eval(self, env):
        obj, _ = self.obj.eval(env)
        if self.start is not None:
            start, _ = self.start.eval(env)
        else:
            start = None
        if self.end is not None:
            end, _ = self.end.eval(env)
        else:
            end = None
        assert type(obj) in [str, list, tuple], 'Not a sliceable item'
        assert (type(start) == int or start is None) and (type(end) == int or end is None), "Slice indices must be integers"
        if start is not None and end is not None:
            return obj[start:end], env
        if start is not None:
            return obj[start:], env
        if end is not None:
            return obj[:end], env
        return obj[:], env


class BTrue(Expr):
    def eval(self, env):
        return True, env

    def __str__(self):
        return "true"

    def __eq__(self, other):
        return isinstance(other, BTrue)

    def __hash__(self):
        return hash(True)


class BFalse(Expr):
    def eval(self, env):
        return False, env

    def __str__(self):
        return "false"

    def __eq__(self, other):
        return isinstance(other, BFalse)

    def __hash__(self):
        return hash(False)


class Var(Expr):
    def __init__(self, var):
        assert isinstance(var, str), f"{var} is not a valid variable name"
        self.name = var

    def eval(self, env):
        try:
            return env[self.name], env
        except KeyError:
            raise UnboundVariable(self.name)

    def __str__(self):
        return str(self.name)


class Class(Expr):
    def __init__(self, name, body, superClass):
        assert isinstance(name, Var), "Class name is invalid"
        assert self.bodyIsOk(body), "Class body can only contain method and variable declarations"
        assert superClass is None or isinstance(superClass, Var), "Invalid syntax when declaring superclass"
        self.name = name
        self.body = body
        self.superClass = superClass

    def bodyIsOk(self, body):
        """
        Returns whether body is a sequence of assignment statements and functions 
        (or alternatively just a single statement of those types)
        """
        if isinstance(body, Assign) or isinstance(body, Function):
            return True
        if not isinstance(body, Seq):
            return False
        # Make sure everything has an access
        if isinstance(body.left, Function) and not isinstance(body.left, AccessFunction):
            body.left = AccessFunction.fromFunc(body.left, PrivacyMod.PUBLIC)
        if isinstance(body.right, Function) and not isinstance(body.right, AccessFunction):
            body.right = AccessFunction.fromFunc(body.right, PrivacyMod.PUBLIC)
        if isinstance(body.left, Assign) and not isinstance(body.left, AccessAssign):
            body.left = AccessAssign.fromAssign(body.left, PrivacyMod.PUBLIC)
        if isinstance(body.right, Assign) and not isinstance(body.right, AccessAssign):
            body.right = AccessAssign.fromAssign(body.right, PrivacyMod.PUBLIC)
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
            return env, {}
        if isinstance(body, Function):
            # Evaluate the function to get the environment mapping func name to closure
            _, env = body.eval({})
            return {}, env
        leftClassVars, leftMethods = self.destructBody(body.left)
        rightClassVars, rightMethods = self.destructBody(body.right)
        return {**leftClassVars, **rightClassVars}, {**leftMethods, **rightMethods}

    def eval(self, env):
        if self.superClass is not None:
            superClass = env[self.superClass.name]
        else:
            superClass = None
        classInfo = ClassInfo(self.name.name, *self.destructBody(self.body), superClass)
        env[self.name.name] = classInfo
        return classInfo, env


class Dot(Expr):
    def __init__(self, obj, attr):
        assert isinstance(obj, Expr), "Left side of a dot operator must be an expression"
        assert isinstance(attr, Var), f"Right side of a dot operator must be a variable, {attr} is not"
        self.obj = obj
        self.attr = attr

    def eval(self, env):
        attr = self.attr.name
        classInfo, newEnv = self.obj.eval(env)
        if self.obj.name == 'super':
            (obj, cls) = classInfo
            return cls[attr][0][0].methodify(obj), newEnv

        val = classInfo[attr]
        owner = AttrOwner.THIS
        if isinstance(val, tuple):
            val, owner = val
        if isinstance(val, tuple) and isinstance(val[0], Closure) and \
                (isinstance(classInfo, Object) or isinstance(classInfo, PrivateObject)):
            clos, access = val
            if access != PrivacyMod.PUBLIC and not isinstance(classInfo, PrivateObject):
                raise TypeError("Attempted to access private method in public context!")
            return clos.methodify(classInfo), newEnv
        if isinstance(val, tuple):
            if isinstance(val[0], tuple):
                val, owner = val
            v, access = val
            if access != PrivacyMod.PUBLIC and not isinstance(classInfo, PrivateObject):
                raise TypeError("Attempted to access private variable in public context!")
            return v, newEnv
        return val, newEnv

    def __str__(self):
        return f"{self.obj}.{self.attr}"


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


class AccessFunction(Function):
    def __init__(self, name, params, exp, access):
        super().__init__(name, params, exp)
        assert isinstance(access, PrivacyMod)
        self.access = access

    @classmethod
    def fromFunc(cls, function, access):
        assert isinstance(function, Function)
        return AccessFunction(function.name, function.args, function.exp, access)

    def eval(self, env):
        clos = Closure(self.exp, self.args, env.copy())
        clos.env[self.name.name] = clos, self.access
        env[self.name.name] = clos, self.access
        return clos, env


class AnonFunction(Expr):
    def __init__(self, params, exp):
        for p in params:
            assert isinstance(p, Var)
        assert isinstance(exp, Expr)
        self.args = params
        self. exp = exp

    def eval(self, env):
        clos = Closure(self.exp, self.args, env.copy())
        return clos, env

    def __str__(self):
        args = ' '.join(map(str, self.args))
        return f"fun {args} -> {self.exp}"


class App(Expr):
    def __init__(self, func, args):
        assert isinstance(func, Expr) or isinstance(func, AnonFunction)
        for a in args:
            assert isinstance(a, Expr)
        self.func = func
        self.args = args

    def eval(self, env):
        clos, env1 = self.func.eval(env)
        # Handle class methods
        if isinstance(clos, tuple):
            print(clos)
            clos, _ = clos
        if isinstance(clos, Closure):
            # Copy the args, and if we have a method call, insert the object for "this"
            newArgs = self.args.copy()
            if isinstance(clos, MethodClosure):
                newArgs.insert(0, clos.obj)
            if len(clos.args) != len(newArgs):
                raise TypeError("Number of arguments does not match number of parameters")
            env2 = {k.name: v.eval(env)[0] for (k, v) in zip(clos.args, newArgs)}
            if isinstance(clos, MethodClosure):
                env2['this'] = PrivateObject(env2['this'])
                if 'super' in env:
                    superClass = env['super'][1].superClass if env['super'][1] else None
                else:
                    superClass = clos.obj.superClass
                env2['super'] = (clos.obj, superClass)
            return clos.expr.eval({**env2, **clos.env})[0], env1
        # Handle constructor calls
        if isinstance(clos, ClassInfo):
            # Create a new object
            obj = clos(self.args, env)
            return obj, env1

        raise NotAFunction(self.func)

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


class Null(Expr):
    def eval(self, env):
        return None, env

    def __str__(self):
        return "null"


class Skip(Expr):
    def eval(self, env):
        return (), env

    def __str__(self):
        return "skip"


class Assign(Expr):
    def __init__(self, var, exp):
        assert isinstance(var, Var) or isinstance(var, Dot) or isinstance(var, Index) or isinstance(var, Slice), "Left side of an assignment statement must support assignment"
        assert isinstance(exp, Expr)
        self.var = var
        self.exp = exp

    def eval(self, env):
        if isinstance(self.var, Var):
            env[self.var.name] = self.exp.eval(env)[0]
        elif isinstance(self.var, Dot):
            (obj, _), attr, (newval, _) = self.var.obj.eval(env), self.var.attr.name, self.exp.eval(env)
            obj[attr] = newval
        elif isinstance(self.var, Index):
            (obj, _), (ind, _), (newval, _) = self.var.obj.eval(env), self.var.ind.eval(env), self.exp.eval(env)
            obj[ind] = newval
        elif isinstance(self.var, Slice):
            if self.var.start is not None:
                start, _ = self.var.start.eval(env)
            else:
                start = None
            if self.var.end is not None:
                end, _ = self.var.end.eval(env)
            else:
                end = None
            (obj, _), (newval, _) = self.var.obj.eval(env), self.exp.eval(env)
            if start is not None and end is not None:
                obj[start:end] = newval
            elif start is not None:
                obj[start:] = newval
            elif end is not None:
                obj[:end] = newval
            else:
                obj[:] = newval
        return (), env

    def __str__(self):
        return f"{self.var} := {self.exp}"


class AccessAssign(Assign):
    def __init__(self, var, exp, access):
        super().__init__(var, exp)
        assert isinstance(access, PrivacyMod)
        self.access = access

    @classmethod
    def fromAssign(cls, assign, access):
        assert isinstance(assign, Assign)
        return AccessAssign(assign.var, assign.exp, access)

    def eval(self, env):
        if isinstance(self.var, Var):
            env[self.var.name] = self.exp.eval(env)[0], self.access
        elif isinstance(self.var, Dot):
            (obj, _), attr, (newval, _) = self.var.obj.eval(env), self.var.attr.name, self.exp.eval(env)
            obj[attr] = newval, self.access
        elif isinstance(self.var, Index) or isinstance(self.var, Slice):
            super().eval(env)
        return (), env


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
        assert b[0], f'Test expression {self.exp} evaluated to false!'
        return (), env

    def __str__(self):
        return f"test({self.exp})"


class Break(Expr):
    pass


class Continue(Expr):
    pass
