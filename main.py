import oomphparse
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='OOOOOOMMPPPHHHHH')
    parser.add_argument('-f', action="store", dest="f", type=str, required=True)

    args = parser.parse_args()
    in_file = args.f

    with open(in_file) as file:
        prog = file.read()
    # print(prog)
    result = oomphparse.parser.parse(prog)
    # print(result)
    env = result.eval({})


if __name__ == "__main__":
    main()
