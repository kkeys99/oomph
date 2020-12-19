# OOMPH

### Introduction 

OOMPH is an Object Oriented iMPerative language that provides classic 
object oriented features such as the ability to create classes and 
subclasses and to restrict the access of class variables and methods. 
All variables in OOMPH are mutable. 


## Values 

Values in OOMPH are ints, booleans, strings, null, tuples, lists, 
and dictionaries: 

```
v := n
    | b
    | s
    | (v1, v2, ..., vn)
    | [v1, v2, ..., vn]
    | {k1: v1, K2: v2, ..., kn: vn} 
    | null
```

### Arithmetic Expressions 

Arithmetic expressions include: 

```
aexp := n (integer literals) 
      | n1 + n2 
      | n1 - n2 
      | n1 * n2 
``` 

## Boolean Expressions 

Boolean expressions include:

```
bexp := true 
    | false
    | b1 and b2 
    | b1 or b2
    | a1 < a2
    | a1 <= a2
    | a1 > a2
    | a1 >= a2
    | e1 = e2
    | e1 != e2  
```

## Basic Commands 

Basic commands are imported from the IMP language. They include: 

```
c := skip
    | null 
    | c1; c2
    | x := c 
    | x 
    | test(bexp) 
    | print(c)
    | aexp
    | bexp
    | (c)
    | if (b) {c1} else {c2}
    | while (b) {c}
```

## Function Definition

Functions are defined with a name and a list of arguments. Function definition 
adds the function to the environment and returns null. 
``` 
def <name> (args): {body}
```
A function can also have no arguments: 
```
def <name> (): {body} 
```
Anonymous functions can also be defined, with or without arguments: 
```
fun (args) -> body 
fun () -> body
```
To apply a function, we supply it with a list of arguments. Functions are 
call-by-value. 
```
def f(x): {x + 1}; f(2) ( --> 3)
(fun (x, y, z) -> (x + y + z))(3, 5, 7) (--> 15) 
```

## Collections

OOMPH provides built in strings, tuples, lists, and dictionaries that 
behave like their Python counterparts. Tuples, lists, and dictionaries 
are not homogeneous. 

```
s := "hello world"; s[-5:-1] (--> "worl")
s := "Hello" + " world" (--> "Hello world")

t := (true, 2); t[0] (--> true)
t := (3, 4) + (3) + () (--> (3, 4, 3)) 

l := [1, 2, 3, 4]; l[1:3] (--> [2, 3])
l := [1, 2] + [3, 4] (--> [1, 2, 3, 4]
l := [[1, 2], [true, false]]; l[0][1] (--> 2) 

d := {1: 'a', 2: 'b'}; d[1] (--> 'a')
```

## Classes 

Classes are the primary feature of OOMPH. Classes are 
defined as a sequence of assignments: 

```
class Foo: {
    x := 1;
    def y(z): {z}
}; 
f := Foo(); f.y(f.x) (--> 1) 
```

If no constructor is provided, the class essentially serves 
as a struct for the variables and methods inside. 

If a function named 'constructor' is supplied, then it 
will be called when new objects are made. 

```
class Bar: {
    def constructor(this, x): {
        this.x := x
    }; 
}; b := Bar(1); b.x (--> 1)
``` 
If a method requires a parameter named 'this,' then it will be 
substituted with the instance calling the method when it is called. 

```
class Baz: {
    def constructor(this, x): {
        this.x := x
    }; 
    def foo(this, y): {
        this.x + y
    }
}; b = Baz(1); b.foo(3) (--> 4)  
```

## Inheritance 

Classes can extend another class. The subclass inherits all (public)
methods and variables from the super class, and can call them as if they 
belonged to the subclass (more on access restriction next). 

```
class A: {
    a := 4; 
    def foo(this, x): {
        this.a + x
    }
}; 
class B(A): {
    a := 5
}; 
b := B(); b.foo(5) (--> 10, not 9)
``` 

## Access Restriction 

Classes can restrict access with the public, protected, and private 
keywords. If no access modifier is specified, access defaults to 
public. 

```
class A: {
    a private := 4; 
    def public getA(this): {
        this.a
    }
}; 
a := A(); a.getA() (--> 4); a.a (--> error!)
```

Subclasses can access any public or protected elements from the superclass: 
```
class A: {
    a private := 4; 
    b protected := 5;
    def public getA(this): {
        this.a
    }
}; 
class B(A): {
    def public getB(this): {
        this.b
    };
    def public getA(this):{
        this.a
    } 
};
b := B(); b.getB() (--> 5); b.getA() (--> error!)
```

There is a known issue where subclasses can not call 
superclass methods that reference private fields - we tried fixing this 
by passing the "owner" of a function in the eval function, but we 
didn't have time to finish this. 