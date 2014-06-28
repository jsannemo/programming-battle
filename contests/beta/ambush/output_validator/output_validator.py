import sys
import re

test_case = open(sys.argv[1], "r")
team_output = open(sys.argv[2], "r")

int_pat = "^(0|[1-9][0-9]*)$"
line = team_output.readline()
assert re.match(int_pat, line)
team_ans = int(line)
line = team_output.readline()
assert len(line) == 0

l, a, b, p = [int(x) for x in test_case.readline().split()]

a, b = [min(a, b), max(a, b)]

between = False

# If horse is to the left or right, he can only run to an endpoint
if p < a:
    p = 0
elif p > b:
    p = l
else:
    between = True


optimal = 0

# Make cows go together
while b - a > 2:
    b-=1
    a+=1
    optimal+=1

# If horse is at endpoint, make them go there
if not between:
    if p == 0:
        optimal += (b-a-1) + a
    if p == l:
        optimal += (b-a-1) + (l - b)
else:
    # If there is a space between cows, make sure they minimize the max dist
    if b - a == 2:
        if a > l - b:
            b-=1
        else:
            a+=1
        optimal+=1
    # Horse choose the maximum dist
    optimal += max(a, l - b)

if optimal != team_ans:
    print("Expected %d got %d" % (optimal, team_ans))
    sys.exit(43)

sys.exit(42)
