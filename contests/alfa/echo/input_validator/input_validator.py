import sys

test = sys.stdin.readline()
assert len(test) > 1

assert len(sys.stdin.readline()) == 0

sys.exit(42)
