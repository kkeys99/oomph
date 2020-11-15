import os
import oomphparse

def test():
    testDir = os.path.join(os.getcwd(), 'tests')
    tests = os.listdir(testDir)
    tests.sort()
    for filename in tests:
        print(filename)
        with open(os.path.join(testDir, filename)) as testFile:
            prog = testFile.read()
        result = oomphparse.parser.parse(prog)
        print(result.eval({}))


if __name__ == "__main__":
    test()