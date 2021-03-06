from time import sleep
from datetime import datetime
import pytz

from battle.models import Session, Contest, Team, Problem, Solution, TestCase, Solution, Judgement
from battle.api import Language, Status, Verdict
from battle.backend.run import InputValidator, OutputValidator, SolutionProgram

class JudgeDaemon:

    def start(self):
        sess = Session()
        while True:
            solutions = sess.query(Solution).from_statement("SELECT * FROM solution WHERE status = :queued ORDER BY submission_time ASC").params(queued=Status.queued.name).all()
            testcases = sess.query(TestCase).from_statement("SELECT * FROM testcase WHERE status = :queued ORDER BY submission_time ASC").params(queued=Status.queued.name).all()

            for testcase in testcases:
                self.validate_testcase(sess, testcase)

            while len(solutions) + len(testcases) > 0:
                next_solution = None if len(solutions) == 0 else solutions[0]
                next_testcase = None if len(testcases) == 0 else testcases[0]
                if next_testcase and (not next_solution or next_testcase.submission_time <= next_solution.submission_time):
                    self.judge_testcase(sess, next_testcase)
                    testcases = testcases[1:]
                else:
                    self.judge_solution(sess, next_solution)
                    solutions = solutions[1:]
            sleep(1)

    # TODO run the testcase on the solutions to get the time limit
    def validate_testcase(self, sess, testcase):
        validator = InputValidator(testcase.problem)
        validator.compile()
        if not validator.validate(testcase.contents):
            testcase.status = Status.rejected.name
            sess.commit()

    def judge_testcase(self, sess, testcase):
        if testcase.status == Status.rejected.name:
            return
        print("Juding test case %d" % testcase.testcase_id)
        solutions = sess.query(Solution).from_statement("SELECT * FROM solution WHERE problem_id = :problem AND submission_time < :submission AND status = :active ORDER BY submission_time ASC") \
            .params(problem=testcase.problem.problem_id, submission=testcase.submission_time, active = Status.active.name).all()

        output_validator = OutputValidator(testcase.problem)
        output_validator.compile()
        for solution in solutions:
            program = SolutionProgram(solution)
            program.compile()
            judgement = self.judge(sess, output_validator, program, solution, testcase)
            if not judgement.get_verdict() == Verdict.solved:
                self.transition(sess, solution, Status.defeated.name)
                print("Solution %d defeated" % solution.solution_id)

        testcase.status = Status.active.name
        sess.commit()

    def judge(self, sess, output_validator, program, solution, testcase):
        print("Testing solution %d with case %d" % (solution.solution_id, testcase.testcase_id))
        # TODO do the test with the correct limit!
        judgement = Judgement(testcase=testcase, solution=solution)
        result = program.test(testcase.contents)

        if result.time_limit_exceeded:
            judgement.verdict = Verdict.time_limit_exceeded.name
        elif result.run_time_error:
            judgement.verdict = Verdict.run_time_error.name
        else:
            if not output_validator.validate(testcase.contents, result.stdout):
                judgement.verdict = Verdict.wrong_answer.name
            else:
                judgement.verdict = Verdict.solved.name
        judgement.runtime = result.time
        judgement.memory = result.memory
        print("Result: %s" % judgement.verdict)
        sess.add(judgement)
        sess.commit()
        return judgement


    def transition(self, sess, solution, new_status):
        solution.status = new_status
        sess.commit()

    def judge_solution(self, sess, solution):
        problem = solution.problem
        print("Judging solution %d" % solution.solution_id)
        test_cases = sess.query(TestCase).from_statement("SELECT * FROM testcase WHERE problem_id = :problem AND submission_time <= :submission AND status = :active ORDER BY submission_time ASC") \
            .params(problem=problem.problem_id, submission=solution.submission_time, active=Status.active.name).all()

        self.transition(sess, solution, Status.testing.name)

        output_validator = OutputValidator(solution.problem)
        output_validator.compile()

        program = SolutionProgram(solution)
        if not program.compile():
            self.transition(sess, solution, Status.rejected.name)
            # TODO show this to teams
            error = program.compiler_output
            return
        for testcase in test_cases:
            judgement = self.judge(sess, output_validator, program, solution, testcase)
            if judgement.verdict != Verdict.solved.name:
                self.transition(sess, solution, Status.failed.name)
                return

        previous = sess.query(Solution).filter_by(team=solution.team, problem=solution.problem, status=Status.active.name).all()
        for prev in previous:
            self.transition(sess, prev, Status.inactive.name)
        self.transition(sess, solution, Status.active.name)
        print("Status: %s" % solution.status)


def start():
    daemon = JudgeDaemon()

    daemon.start()
