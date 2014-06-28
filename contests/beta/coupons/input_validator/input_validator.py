import sys
import re

int_pat = "(0|[1-9][0-9]*)"

line = sys.stdin.readline()
assert re.match("^" + int_pat + "$", line)
n = int(line)
assert 0 <= n <= 50000

last_t = -1

for i in range(n):
    line = sys.stdin.readline()
    assert re.match("^" + int_pat + " " + int_pat + "$", line)
    z, t = [int(x) for x in line.split()]
    assert 0 <= z <= 10
    assert last_t < t <= 1000000000
    last_t = t

line = sys.stdin.readline()
assert len(line) == 0

sys.exit(42)
