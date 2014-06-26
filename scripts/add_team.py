#!/usr/bin/env python3
from sys import argv
import random
import string

from battle.models import Session, Team


def random_string():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

def add_team(sess, contest_id, team_name):
    solver_login = random_string()
    solver_password = random_string()
    tester_login = random_string()
    tester_password = random_string()

    team = Team(contest_id=contest_id, team_name=team_name, solver_login=solver_login, solver_password=solver_password,
            tester_login=tester_login, tester_password=tester_password)


    print("Team: %s\nTester login: %s\nTester password:%s\n\n\n\nTeam: %s\nSolver login: %s\nSolver password: %s"%
            (team_name, tester_login, tester_password, team_name, solver_login, solver_password))
    sess.add(team)



def main():
    contest_id = argv[1]
    team_name = argv[2]
    s = Session()
    add_team(s, contest_id, team_name)
    s.commit()


if __name__ == '__main__':
    main()
