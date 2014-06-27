import sys

arguments = sys.argv

test_case = open(arguments[1], "r").read()
team_output = open(arguments[2], "r").read()

if team_output != test_case:
    sys.exit(43)
else:
    sys.exit(42)
