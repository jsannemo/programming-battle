import sys
import re

int_pat = "(0|[1-9][0-9]*)"
line_pat = "^" + ' '.join([int_pat]*4) + "$"

line = sys.stdin.readline()
assert re.match("^" + line_pat + "$", line)
l, a, b, p = [int(x) for x in line.split()]

assert 1 <= l <= 1000
assert 0 <= a <= l
assert 0 <= b <= l
assert 0 <= p <= l

assert len(set([a, b, p])) == 3

line = sys.stdin.readline()

assert len(line) == 0

sys.exit(42)
