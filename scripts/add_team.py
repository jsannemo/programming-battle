#!/usr/bin/env python3
from sys import argv
import random
import string

from battle.models import Session, Team, Author
from battle.api import Role


def random_string():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

def add_author(sess, team, role):
    username = random_string()
    password = random_string()

    print('Role: %s' % role.name)
    print('Username: %s' % username)
    print('Password: %s' % password)

    author = Author(
            team_id = team.team_id,
            username = username,
            password = password,
            role = role.name,
        )

    sess.add(author)


def add_team(sess, contest_id, team_name):
    solver_username = random_string()
    solver_password = random_string()
    tester_username = random_string()
    tester_password = random_string()

    team = Team(
            contest_id=contest_id,
            name=team_name,
        )

    sess.add(team)
    sess.flush()

    print('Team: %s' % team_name)
    add_author(sess, team, Role.solver)
    print('')

    print('Team: %s' % team_name)
    add_author(sess, team, Role.tester)


def main():
    contest_id = argv[1]
    team_name = argv[2]
    s = Session()
    add_team(s, contest_id, team_name)
    s.commit()


if __name__ == '__main__':
    main()
