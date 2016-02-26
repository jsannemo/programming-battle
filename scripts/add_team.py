#!/usr/bin/env python3
from sys import argv
import random
import string

from battle.models import Session, Team
from battle.api import Role


def random_string():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

def add_team(sess, contest_id, team_name):
    username = random_string()
    password = random_string()

    team = Team(
            contest_id=contest_id,
            name=team_name,
            username=username,
            password=password,
        )

    sess.add(team)
    sess.flush()

    print('Team: %s' % team_name)
    print('Username: %s' % username)
    print('Password: %s' % password)

def main():
    contest_id = argv[1]
    team_name = argv[2]
    s = Session()
    add_team(s, contest_id, team_name)
    s.commit()


if __name__ == '__main__':
    main()
