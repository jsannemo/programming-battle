from datetime import datetime
import pytz

from .base import BaseHandler
from battle.models import Solution
from battle.api import Status, Verdict

from collections import defaultdict

# TODO: move these to contest settings
DEFEAT_SCORE = 1000

class StandingsHandler(BaseHandler):

    # TODO cache this
    def get(self):
        submissions = []
        testcases = []

        for problem in self.contest.problems:
            submissions += problem.solutions
            testcases += problem.testcases

        submissions = sorted(submissions, key=lambda s: s.submission_time)
        testcases = sorted(testcases, key=lambda s: s.submission_time)

        standings = Standings(self.contest)
        standings.add_teams(self.contest.teams)
        standings.add_submissions(submissions, testcases)

        ordered_teams = [t for t in self.contest.teams]
        ordered_teams = sorted(ordered_teams, key=lambda team: -standings.get_team_score(team.team_id))

        self.set('ordered_teams', ordered_teams)
        self.set('s', standings)

        self.template('standings/view.html')

class Standings:
    def __init__(self, contest):
        self.contest = contest
        self.teams = {}
        self.cases = []
        self.solutions = set()

    def get_team_score(self, team_id):
        team_standings = self.teams[team_id]
        score = 0
        for problem in self.contest.problems:
            score += team_standings.solve_score(problem) + team_standings.test_score(problem)
        return score

    def add_teams(self, teams):
        for team in teams:
            self.teams[team.team_id] = TeamStanding(self.contest, team)

    def add_submissions(self, solutions, tests):
        now = datetime.now(pytz.utc)
        while len(solutions) + len(tests):
            which = None
            if not solutions:
                which = False
            elif not tests:
                which = True
            else:
                which = solutions[0].submission_time < tests[0].submission_time

            if which:
                self.process_solution(solutions[0])
                solutions = solutions[1:]
            else:
                self.process_testcase(tests[0])
                tests = tests[1:]
        for submission in list(self.solutions):
            end = min(now, self.contest.get_end_time())
            self.stop_scoring(submission, end)

    def process_solution(self, solution):
        team = self.teams[solution.team.team_id]
        team.add_solution(solution)
        for case in self.cases:
            judgement = solution.get_judgement_for(case)
            if not judgement: continue
            if judgement.verdict != Verdict.solved.name:
                return
        for other in list(self.solutions):
            if solution.team == other.team and solution.problem == other.problem:
                self.stop_scoring(other, solution.submission_time)
        self.solutions.add(solution)

    def stop_scoring(self, solution, time):
        # TODO how should this scoring work?
        score = int((time - solution.submission_time).total_seconds())
        self.teams[solution.team.team_id].score_submission(solution.problem, score)
        self.solutions.remove(solution)

    def process_testcase(self, case):
        if case.status == Status.rejected.name: return
        survived = set()
        for solution in list(self.solutions):
            judgement = solution.get_judgement_for(case)
            if judgement and judgement.verdict != Verdict.solved.name:
                self.stop_scoring(solution, case.submission_time)
                self.teams[case.team].score_test(case.problem)
                continue
        self.cases.append(case)

    def __getitem__(self, index):
        return self.teams[index]

class TeamStanding:
    def __init__(self, contest, team):
        self.contest = contest
        self.team = team
        self.solve_scores = defaultdict(int)
        self.test_scores = defaultdict(int)
        self.solutions = {}

    def solve_score(self, problem):
        return self.solve_scores[problem.problem_id]

    def test_score(self, problem):
        return self.test_scores[problem.problem_id]

    def score_test(self, problem):
        self.test_scores[problem.problem_id] += 1000

    def score_submission(self, problem, score):
        self.solve_scores[problem.problem_id] += score

    def add_solution(self, solution):
        problem = solution.problem.problem_id
        previous = [None if problem not in self.solutions else self.solutions]
        if solution.get_status() == Status.testing or solution.get_status() == Status.active:
            self.solutions[problem] = solution
        elif solution.get_status() == Status.defeated and (previous is None or previous.status in [Status.defeated, Status.rejected]):
            self.solutions[problem] = solution
        elif solution.get_status() == Status.rejected and (previous is None or previous.status in [Status.rejected]):
            self.solutions[problem] = solution

    def get_solution(self, problem_id):
        if problem_id in self.solutions:
            return self.solutions[problem_id]
        return None

    def __getitem__(self, index):
        if index == 'score':
            score = 0
            for x, y in list(self.test_scores.items()) + list(self.solve_scores.items()):
                score += y
            return score
        elif index == 'solver_score':
            score = 0
            for x, y in self.solve_scores.items():
                score += y
            return score
        elif index == 'tester_score':
            score = 0
            for x, y in self.test_scores.items():
                score += y
            return score
        elif index in self.solutions:
            return { 'solution': self.solutions[index] }
        else:
            return {}
