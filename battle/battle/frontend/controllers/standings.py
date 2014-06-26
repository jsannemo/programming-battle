from datetime import datetime
import pytz

from .base import BaseHandler
from battle.models import Solution
from battle.api import Status

# TODO: move these to contest settings
DEFEAT_SCORE = 100

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
                problem_id = solution.problem_id
                if not 'solution' in s[team.team_id][problem_id] and not solution.status == Status.rejected.name:
                    s[team.team_id][problem_id]['solution'] = solution

        for team in self.contest.teams:
            for solution in team.solutions:
                for event in solution.events:
                    if event.new_status == Status.defeated.name:
                        s[event.testcase.team.team_id]['score'] += DEFEAT_SCORE
                    if event.old_status == Status.active.name:
                        start = solution.solution_time - self.contest.start_time
                        end = event.event_time - self.contest.start_time
                        score = int((end - start).total_seconds())
                        s[team.team_id]['score'] += score
                if solution.status == Status.active.name:
                    start = solution.solution_time - self.contest.start_time
                    end = now - self.contest.start_time
                    score = int((end - start).total_seconds())
                    s[team.team_id]['score'] += score

        self.set('s', s)

        self.template('standings/view.html')
