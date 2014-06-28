from datetime import datetime
import pytz

from .base import BaseHandler
from battle.models import Solution
from battle.api import Status

# TODO: move these to contest settings
DEFEAT_SCORE = 1000

class StandingsHandler(BaseHandler):

    # TODO cache this
    def get(self):
        now = datetime.now(pytz.utc)

        s = {}
        for team in self.contest.teams:
            s[team.team_id] = {'score': 0}
            for problem in self.contest.problems:
                s[team.team_id][problem.problem_id] = {}
            for solution in team.solutions:
                if solution.solution_time > self.contest.get_end_time():
                    continue
                problem_id = solution.problem_id
                if not 'solution' in s[team.team_id][problem_id] or (s[team.team_id][problem_id]['solution'].status == Status.rejected.name and solution.status != Status.rejected.name):
                    s[team.team_id][problem_id]['solution'] = solution

        for team in self.contest.teams:
            for solution in team.solutions:
                if solution.solution_time > self.contest.get_end_time():
                    continue
                for event in solution.events:
                    if event.new_status == Status.defeated.name and event.testcase.team != event.solution.team:
                        s[event.testcase.team.team_id]['score'] += DEFEAT_SCORE
                    if event.old_status == Status.active.name:
                        start = solution.solution_time - self.contest.start_time
                        end = event.event_time - self.contest.start_time
                        score = int((end - start).total_seconds())
                        s[team.team_id]['score'] += score
                if solution.status == Status.active.name:
                    start = solution.solution_time - self.contest.start_time
                    end = min(now, self.contest.get_end_time()) - self.contest.start_time
                    score = int((end - start).total_seconds())
                    s[team.team_id]['score'] += score

        ordered_teams = [t for t in self.contest.teams]
        ordered_teams = sorted(ordered_teams, key=lambda team: -s[team.team_id]['score'])

        self.set('ordered_teams', ordered_teams)
        self.set('s', s)

        self.template('standings/view.html')
