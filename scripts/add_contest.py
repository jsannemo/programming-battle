#!/usr/bin/env python3
import yaml
from sys import argv
import os.path
import shutil

from battle.models import Session, Contest, Problem
from battle.util.config import config
from scripts.add_team import add_team

def sure():
    ans = input()
    if not len(ans) or ans[0] != 'y':
        print("Quiting")
        return False
    return True


def add_problem(sess, contest, contest_config, problem_path):
    tag = os.path.basename(problem_path)

    problem_config = yaml.safe_load(open(os.path.join(problem_path, "problem.yaml")).read())
    index = contest_config['order']

    existing = sess.query(Problem).filter_by(tag=tag, contest = contest).all()

    if existing:
        problem = existing[0]
        print("A problem with tag %s already exists. Update? (y/n)" % tag)
        if not sure():
            return
        problem.name = problem_config['name']
        problem.available_from = contest_config['available_from']
        problem.contest = contest
        problem.contest_order = index

    else:
        print("Adding problem %s (%s)" % (tag, problem_config['name']))
        problem = Problem(name = problem_config['name'], tag = tag, available_from = contest_config['available_from'], contest = contest, contest_order = index)

        sess.add(contest)

    install_path = os.path.join(config.problem_directory, contest.tag, problem.tag)
    try:
        shutil.rmtree(install_path)
    except:
        pass
    shutil.copytree(problem_path, install_path)

def main():
    if len(argv) < 2:
        print("You need to specify the location of the contest directory")
    contest_directory = argv[1]
    print(contest_directory)
    contest_tag = os.path.basename(contest_directory)
    print("Contest tag %s" % contest_tag)

    contest_config = yaml.safe_load(open(os.path.join(contest_directory, "contest.yaml")).read())

    # Add contest
    sess = Session()
    existing = sess.query(Contest).filter_by(tag=contest_tag).all()
    if existing:
        contest = existing[0]
        print("A contest with this tag already exists. Update? (y/n)")
        if not sure():
            return
        contest.name = contest_config['name']
        contest.tag = contest_tag
        contest.start_time = contest_config['start']
        contest.length = contest_config['length']

    else:
        print("Adding contest %s (%s)" % (contest_tag, contest_config['name']))
        print("Start time %s" % contest_config['start'])
        print("Length %s" % contest_config['length'])

        contest = Contest(name = contest_config['name'], tag = contest_tag, start_time = contest_config['start'], length = contest_config['length'])

        sess.add(contest)

    # Add problems

    added = []
    print("Adding problems")
    for problem, config in contest_config['problems'].items():
        add_problem(sess, contest, config, os.path.join(contest_directory, problem))
        added.append(problem)
    remaining = sess.query(Problem).filter(~Problem.tag.in_(added)).filter_by(contest = contest).all()
    for problem in remaining:
        print("Found additional problem %s (%s). Remove? (y/n)" % (problem.tag, problem.name))
        if sure():
            sess.delete(problem)

    existing_teams = [team.team_name for team in contest.teams]
    print("\n\n")
    for team in open(os.path.join(contest_directory, "teams"), "r").readlines():
        if team not in  existing_teams:
            add_team(sess, contest.contest_id, team)
            print("\n\n\n\n")
    print("\n\n")

    sess.commit()

if __name__ == '__main__':
    main()
