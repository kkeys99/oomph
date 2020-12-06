# OOMP(H)

### Vision

Our general goal for the project is to create an extended version of IMP in 
Python with object-oriented features. As such, we have decided to name our 
language OOMP(H), for objected oriented MP (H added for memorability). The 
major feature we hope to add is class declarations. This includes adding 
constructs such as instance variables, private and static methods and class 
variables, and some sort of class inheritance, if time allows towards the end 
of the project.

### Status

So far, we have implemented all of IMP and extended it with (potentially 
recursive) functions, anonymous functions, and classes. The simplest class can 
be defined as follows: 

```
class Dog: {
    name := 5;
    value := 10;
    type := 3;
    def woof(x): { x };
    def wag(y): { y + 1 }
};
```

Class Dog essentially serves as a struct - variables and functions can be
accessed as `Dog.woof(Dog.name)` (=5). No explicit constructor is provided, but
Dog elements can still be made as follows: `d := Dog(); d.name = 6`. 
Classes can also have custom constructors as follows:  

```
class Student: {
    universityId := 538;
    def constructor(this, sid, gpa, smart): {
        this.sid := sid + 1;
        this.gpa := gpa;
        this.smart := smart
    }
};
```

In this case, the call `s := Student(000, 3.2, true)` calls the constructor 
function to generate a new student object. 

#### Usage 

To run an OOMP(H) file, simply execute `main.py` giving the file to run as an argument:

```
python main.py -f input.oomph
```

You can also run the interpreter interactively by executing `repl.py`. Files in
 the tests directory can be run by executing `test.py`.

### Next Steps

For the final phase of the project, we plan on extending the class semantics with 
access modifiers (private, public, and static) and to implement a Java-esque class
hierarchy with subclassing and interfaces. We also hope to provide a full user 
manual, as well as an implementation of basic data structures to create a more 
complete language. 