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

atk = sorted([int(x) for x in test_case.readline().split()])
atk_s = [int(x) for x in test_case.readline().split()]
def_s = [int(x) for x in test_case.readline().split()]

# Sorted by how quickly we want to kill them
cards = sorted([(atk_s[i], -def_s[i]) for i in range(5)], reverse=True)

optimal = 0

new_cards = []
for card in cards:
    a, d = card
    killed = False
    for j in range(len(atk)):
        if atk[j] > -d:
            killed = True
            del atk[j]
            break
    if not killed:
        new_cards.append(a)

new_cards = sorted(new_cards, reverse=True)

for card in new_cards:
    if card > atk[0]:
        optimal += card - atk[0]
        atk = atk[1:]
    else:
        break

if optimal != team_ans:
    print("Expected %d got %d" % (optimal, team_ans))
    sys.exit(43)

sys.exit(42)
