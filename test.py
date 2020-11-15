import os
import oomphparse

def test():
    testDir = os.path.join(os.getcwd(), 'tests')
    tests = os.listdir(testDir)
    tests.sort()
    for filename in tests:
        with open(os.path.join(testDir, filename)) as testFile:
            prog = testFile.read()
        _ = oomphparse.parser.parse(prog)
        print(f'{filename} OK')


if __name__ == "__main__":
    test()