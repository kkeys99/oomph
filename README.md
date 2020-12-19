# OOMP(H)

An extension of the classic IMP language with object oriented features. Developed for the final project of CS4110 at Cornell University.

## Getting Started

### Prerequisites

The only prerequisites are Python 3.7+ and the [PLY](https://github.com/dabeaz/ply) library, which can be installed using pip.

### Running OOMP(H)

To run an OOMP(H) file, simply execute `main.py` giving the file to run as an argument:

```
python main.py -f input.oomph
```

You can also run the interpreter interactively by executing `repl.py`. Files in the tests directory can be run by executing `test.py`. A manual explaining basic OOMPH syntax can be found in manual.md. 

### Demo

A simple demo for the language can be seen by executing `demo.py` as a script. It reads in the program from `demo.oomph`, making use of a simple PhD class.
The PhD class has some simple methods such as gotAfter, which returns true if the object you call the method on got their PhD after the argument, and areSiblings,
which returns true if the object you call the method on is an intellectual sibling of the argument (i.e. they share an advisor).
Here are some examples of what you can do with the variables loaded in to the demo:

```
gries.gotAfter(church)
walker.gotAfter(gries)
clarkson := PhD("Michael Clarkson", 3, 2010, gries, null)
clarkson.areSiblings(walker)
```

To exit the demo, simply press the EOF key on your keyboard.
