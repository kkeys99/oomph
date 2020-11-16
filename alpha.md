# OOMP(H)

#### Vision

Our general goal for the project is to create an extended version of IMP in Python with object-oriented features. As such, we have decided to name our language OOMP(H), for objected oriented MP (H added for memorability). The major feature we hope to add is class declarations. This includes adding constructs such as instance variables, private and static methods and class variables, and some sort of class inheritance, if time allows towards the end of the project.

#### Status

So far, we have mainly been working on porting the homework 3 implementation of IMP over to Python, without the break and continue commands. Since we are not using OCaml, a large portion of this project sprint involved writing a lexer and parser using the Python [PLY](https://github.com/dabeaz/ply) library and determining how to best create an AST representation using Python classes instead of OCaml variants. We also ported the eval function over to its Python equivalent, implemented a simple REPL, and added functions to our extension of the language.

#### Next Steps

For the beta phase of our project, we plan on determining the precise semantics for class definitions, and adding them to the language. The concrete goals we hope to achieve include the ability to instantiate objects of a class, define and access class variables, create instance attributes for objects, and call methods of a class. In the last portion of the project, we will add Java-esque access modifiers such as static or private methods and variables.
