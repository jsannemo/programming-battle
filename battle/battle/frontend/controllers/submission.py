from datetime import datetime
import pytz
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from .base import BaseHandler, valid_problem, require_login

from battle.models import Problem, Solution, TestCase
from battle.api import detect_language, Role, Status, Language

class SubmitHandler(BaseHandler):

    @require_login
    @valid_problem
    def post(self, problem_tag):

        problem = Problem.find_by_tag(self.db, problem_tag)[0]
        if 'submission' not in self.request.files:
            self.error('Please choose a file')
            return self.redirect('/problem/%s' % problem_tag)

        file_info = self.request.files['submission'][0]
        file_name = file_info['filename']
        file_body = file_info['body'].decode('UTF-8').replace("\r", "")

        now = datetime.now(pytz.utc)
        if self.role == Role.solver:
            language = detect_language(file_name)
            if not language:
                self.error('Invalid language')
                return self.redirect('/problem/%s' % problem_tag)

            sub = Solution(problem_id=problem.problem_id, team_id=self.team_id, language=language.name, status=Status.queued.name, solution_time=now, code=file_body)

            self.db.add(sub)
            self.db.commit()
            self.redirect('/solution/%d' % sub.solution_id)
        else:
            sub = TestCase(problem_id=problem.problem_id, team_id=self.team_id, test=file_body, status=Status.queued.name, testcase_time = now)
            self.db.add(sub)
            self.db.commit()
            self.redirect('/testcase/%d' % sub.testcase_id)

class SolutionViewHandler(BaseHandler):

    def get(self, solution_id):
        try:
            solution_id = int(solution_id)
        except:
            self.error("Invalid solution")
            return self.redirect("/")
        solution = self.db.query(Solution).get(solution_id)
        if not solution or solution.problem.contest != self.contest:
            self.error('Invalid solution')
            return self.redirect('/')

        lexer = get_lexer_by_name(solution.language, stripall=True)
        formatter = HtmlFormatter(linenos=True, cssclass="source", style="monokai")
        result = highlight(solution.code, lexer, formatter)
        self.set('source_style', formatter.get_style_defs('.source pre'))
        self.set('code', result)
        self.set('solution', solution)
        self.set('display_code', self.logged_in and (self.role == Role.tester or self.team_id == solution.team.team_id))
        self.template('submission/view_solution.html')

class SolutionDownloadHandler(BaseHandler):

    def get(self, solution_id):
        try:
            solution_id = int(solution_id)
        except:
            self.error("Invalid solution")
            return self.redirect("/")

        solution = self.db.query(Solution).get(solution_id)
        if not solution or solution.problem.contest != self.contest:
            self.error('Invalid solution')
            return self.redirect('/')

        if not self.logged_in and (self.role == Role.tester or self.team_id == solution.team.team_id):
            self.error('You are not allowed to download this solution')
            return self.redirect('/')

        self.set_header('Content-Type', 'application/octet-stream')
        # TODO use submitted file name
        self.set_header('Content-Disposition', 'attachment; filename=%s-%d.%s' % (solution.problem.tag, solution.solution_id, Language[solution.language].extension))
        self.write(solution.code)

class TestcaseViewHandler(BaseHandler):

    def get(self, testcase_id):
        try:
            testcase_id = int(testcase_id)
        except:
            self.error("Invalid testcase")
            return self.redirect("/")

        testcase = self.db.query(TestCase).get(testcase_id)
        if not testcase or testcase.problem.contest != self.contest:
            self.error('Invalid testcase')
            return self.redirect('/')


        lexer = get_lexer_by_name("text", stripall=True)
        formatter = HtmlFormatter(linenos=True, cssclass="source", style="monokai")
        result = highlight(testcase.test, lexer, formatter)
        self.set('source_style', formatter.get_style_defs('.source pre'))
        self.set('test', result)
        self.set('testcase', testcase)
        self.set('display_test', self.logged_in and (self.role == Role.tester and self.team_id == testcase.team.team_id))
        self.template('submission/view_testcase.html')

class TestcaseDownloadHandler(BaseHandler):

    def get(self, testcase_id):
        try:
            testcase_id = int(testcase_id)
        except:
            self.error("Invalid testcase")
            return self.redirect("/")

        testcase = self.db.query(TestCase).get(testcase_id)
        if not testcase or testcase.problem.contest != self.contest:
            self.error('Invalid testcase')
            return self.redirect('/')

        if not self.logged_in and (self.role == Role.tester and self.team_id == testcase.team.team_id):
            self.error('You are not allowed to download this solution')
            return self.redirect('/')

        self.set_header('Content-Type', 'application/octet-stream')
        # TODO use submitted file name
        self.set_header('Content-Disposition', 'attachment; filename=' + testcase.problem.tag + '-' + testcase.testcase_id + '.in')
        self.write(testcase.test)


class SolutionListHandler(BaseHandler):

    @valid_problem
    def get(self, problem_tag):
        problem = Problem.find_by_tag(self.db, problem_tag)[0]
        self.set('problem', problem)
        self.template('submission/list_solutions.html')

class TestcaseListHandler(BaseHandler):

    @valid_problem
    def get(self, problem_tag):
        problem = Problem.find_by_tag(self.db, problem_tag)[0]
        self.set('problem', problem)
        self.template('submission/list_testcases.html')
