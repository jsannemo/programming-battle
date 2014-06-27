from sys import stdin
import sys
import re

integer = "(0|-?[1-9]\d*)"

while True:
    line = stdin.readline()
    if len(line) == 0:
        break
    assert re.match(integer + " " + integer + "\n", line)
    [n,m] = [int(x) for x in line.split()]
    assert 0 <= n and n <= 2**63-1
    assert 0 <= m and m <= 2**63-1

# Nothing to report
sys.exit(42)
