import sys
import re

int_pat = "(0|[1-9][0-9]*)"
line_pat = "^" + ' '.join([int_pat]*5) + "$"

line = sys.stdin.readline()
assert re.match("^" + int_pat + "$", line)
val = [int(x) for x in line.split()]
for x in val:
    assert 0 <= val <= 3000

line = sys.stdin.readline()
assert re.match("^" + int_pat + "$", line)
val = [int(x) for x in line.split()]
for x in val:
    assert 0 <= val <= 3000

line = sys.stdin.readline()
assert re.match("^" + int_pat + "$", line)
val = [int(x) for x in line.split()]
for x in val:
    assert 0 <= val <= 3000


line = sys.stdin.readline()
assert len(line) == 0

sys.exit(42)
