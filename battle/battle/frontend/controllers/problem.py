from .base import BaseHandler, valid_problem

from battle.models import Problem

class ProblemListHandler(BaseHandler):

    def get(self):
        # TODO Make sure these are ordered according to their order
        # TODO Ensure current_time >= start + available_from
        problems = self.contest.problems
        self.set('problems', problems)
        self.template('problem/list.html')

class ProblemViewHandler(BaseHandler):

    @valid_problem
    def get(self, problem_tag):
        # TODO Ensure problem is in contest
        # TODO Ensure problem is available

        problem = Problem.find_by_tag(self.db, problem_tag)[0]
        problem_statement = problem.get_statement()
        self.set('problem', problem)
        self.set('problem_statement', problem_statement)
        self.template('problem/view.html')
