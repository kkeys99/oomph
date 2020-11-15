from ply import lex, yacc
import oomphlex
import oomphparse
import ast


def main():
    lexer = lex.lex(module=oomphlex)
    parser = yacc.yacc(module=oomphparse)
    env = {}
    while True:
        text = input("> ")
        if text == "quit()":
            break
        if text == "env()":
            print(env)
            continue
        lexer.end = False
        result = parser.parse(text)
        try:
            v, env = result.eval(env)
            print(">> " + str(v))
        except ast.UnboundVariable as e:
            print(e.message)
        except AttributeError:
            print("Invalid input")

    # print(prog)

    # print(result)


if __name__ == "__main__":
    main()
