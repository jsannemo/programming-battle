#!/usr/bin/env python3
from sys import argv

from battle.models import Session, Problem

def main():
    name = argv[1]
    tag = argv[2]
    contest_id = argv[3]
    available_from = argv[4]
    problem_order = argv[5]

    s = Session()
    s.add(Problem(problem_name=name, problem_tag=tag, contest_id=contest_id, available_from=available_from, problem_order=problem_order))
    s.commit()

if __name__ == '__main__':
    main()
