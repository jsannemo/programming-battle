from .base import BaseHandler, valid_problem

from battle.models import Problem

class ProblemListHandler(BaseHandler):

    def get(self):
        problems = self.contest.problems
        self.set('problems', problems)
        self.template('problem/list.html')

class ProblemViewHandler(BaseHandler):

    @valid_problem
    def get(self, problem_tag):
        problem = Problem.find_by_tag(self.db, problem_tag)[0]

        problem_statement = problem.get_statement()
        self.set('problem', problem)
        self.set('problem_statement', problem_statement)
        self.template('problem/view.html')
