import sys
import re

int_pat = "(0|[1-9][0-9]*)"
ints_pat = "(0|[1-9][0-9]*)( (0|[1-9][0-9]*))*"

line = sys.stdin.readline()
assert re.match("^" + int_pat + "$", line)
v = int(line)
assert 0 <= v <= 100

line = sys.stdin.readline()
assert len(line) > 0
assert re.match("^" + ints_pat + "$", line)
a = [int(x) for x in line.split()]
assert len(a) == v
for x in a:
    assert 0 <= x <= 100

assert len(sys.stdin.readline()) == 0

sys.exit(42)
