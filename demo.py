from ply import lex, yacc
import oomphlex
import oomphparse
import ast


def main():
    parser = yacc.yacc(module=oomphparse)
    with open("demo.oomph") as file:
        prog = file.read()
    demo = parser.parse(prog)
    _, env = demo.eval({})
    while True:
        text = input("> ")
        if text == "quit()":
            break
        if text == "env()":
            print(env)
            continue
        result = parser.parse(text)
        try:
            v, env = result.eval(env)
            print(">> " + str(v))
        except Exception as e:
            print(repr(e))
            print("Invalid input")

    # print(prog)

    # print(result)


if __name__ == "__main__":
    main()
