import os
import oomphparse


def red(skk): return "\033[91m {}\033[00m" .format(skk)


def green(skk): return "\033[92m {}\033[00m" .format(skk)


def test():
    testDir = os.path.join(os.getcwd(), 'tests')
    tests = []
    for r, d, f in os.walk(testDir):
        for file in f:
            if '.oomph' in file:
                tests.append(os.path.join(r, file))
    tests.sort()

    for filename in tests:
        with open(os.path.join(testDir, filename)) as testFile:
            prog = testFile.read()
        relative_file = filename.replace(testDir + '/', '')
        try:
            tree = oomphparse.parser.parse(prog)
            _ = tree.eval({})
            print(f'{relative_file}: ' + green('OK'))
        except:
            print(f'{relative_file}:' + red('NOT OK'))


if __name__ == "__main__":
    test()
