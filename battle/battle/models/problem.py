from sqlalchemy import Column, Integer, Interval, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

import os.path

from . import Base
from battle.util.config import config

class Problem(Base):
    __tablename__ = 'problem'

    problem_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    available_from = Column(Interval, nullable=False)
    contest_id = Column(Integer, ForeignKey('contest.contest_id'))
    contest_order = Column(Integer, nullable=False)

    testcases = relationship('TestCase', backref='problem', order_by='desc(TestCase.testcase_time)')
    solutions = relationship('Solution', backref='problem', order_by='desc(Solution.solution_time)')

    @staticmethod
    def find_by_tag(sess, tag):
        problems = sess.query(Problem).from_statement("SELECT * FROM problem WHERE tag = :tag").params(tag=tag).all()
        return problems

    def is_available(self):
        return self.contest.get_elapsed() > self.available_from

    def get_statement(self):
        path = os.path.join(config.problem_directory, self.contest.tag, self.tag, "problem.html")
        try:
            with open(path, "r") as problem_statement:
                return problem_statement.read()
        except:
            return None

    def get_letter(self):
        return chr(ord('A') - 1 + self.contest_order)


    __table_args__ = ( UniqueConstraint('tag', 'contest_id'), )
