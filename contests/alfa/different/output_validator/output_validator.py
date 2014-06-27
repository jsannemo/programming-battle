import sys

arguments = sys.argv

test_case = open(arguments[1], "r").readlines()
team_output = open(arguments[2], "r").readlines()

if len(test_case) != len(team_output):
    sys.exit(43)

for i in range(len(test_case)):
    a, b = [int(x) for x in test_case[i].split()]
    dif = abs(a - b)
    if dif != int(team_output[i]):
        sys.exit(43)

sys.exit(42)
