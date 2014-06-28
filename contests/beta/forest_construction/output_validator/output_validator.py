import sys
import re

test_case = open(sys.argv[1], "r")
team_output = open(sys.argv[2], "r")

v = int(test_case.readline())
deg = [int(d) for d in test_case.readline().split()]
deg_sum = sum(deg)
zeroes = deg.count(0)

possible = True

if deg_sum%2 == 1:
    possible = False
else:
    c = (2 * (v - zeroes) - deg_sum) // 2
    if c == 0 and (v - zeroes) > 0:
        possible = False
    if c < 0:
        possible = False

line = team_output.readline()
expected = "POSSIBLE\n" if possible else "IMPOSSIBLE\n"

if line != expected:
    print("Wrong response: is possible %s gave %s" % (possible, line))
    sys.exit(43)

if possible:
    edges = deg_sum // 2

    int_pat = "[1-9][0-9]*"
    edge_pat = "^"+int_pat+" "+int_pat+"$"

    adj = [[] for i in range(v)]

    for i in range(edges):
        line = team_output.readline()
        assert re.match(edge_pat, line)
        a, b = [int(x) for x in line.split()]
        assert 1 <= a <= v and 1 <= b <= v
        a-=1
        b-=1
        assert a not in adj[b]
        assert b not in adj[a]
        adj[a].append(b)
        adj[b].append(a)

    seen = [False]*v


    def dfs(at, parent):
        if seen[at]:
            sys.exit(43)
        seen[at] = True
        for x in adj[at]:
            if x != parent:
                dfs(x, at)

    for i in range(v):
        assert len(adj[i]) == deg[i]
        if not seen[i]:
            dfs(i, -1)

line = team_output.readline()
assert len(line) == 0

sys.exit(42)
