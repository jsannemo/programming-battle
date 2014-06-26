from sqlalchemy import create_engine, Column, Integer, DateTime, String, ForeignKey, Enum, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base, StatusEnum, LanguageEnum, VerdictEnum
from battle.api import Language, Status, Verdict


class TestCase(Base):
    __tablename__ = 'testcase'

    testcase_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.team_id'))
    problem_id = Column(Integer, ForeignKey('problem.problem_id'))
    status = Column(StatusEnum, nullable=False)
    test = Column(String, nullable=False)
    testcase_time = Column(DateTime(timezone=True), nullable=False)

    max_judge_time = Column(Float)
    max_judge_mem = Column(Float)

    def get_status(self):
        return Status[self.status]

    events = relationship('SolutionEvent', backref='testcase', order_by='SolutionEvent.event_time')

    judgements = relationship('Judgement', backref='testcase', order_by='desc(Judgement.judgement_id)')


class Solution(Base):
    __tablename__ = 'solution'

    solution_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.team_id'))
    problem_id = Column(Integer, ForeignKey('problem.problem_id'))
    language = Column(LanguageEnum, nullable=False)
    status = Column(StatusEnum, nullable=False)
    code = Column(String, nullable=False)
    solution_time = Column(DateTime(timezone=True), nullable=False)

    def get_status(self):
        return Status[self.status]

    events = relationship('SolutionEvent', backref='solution', order_by='SolutionEvent.event_time')

    judgements = relationship('Judgement', backref='solution', order_by='desc(Judgement.judgement_id)')


class Judgement(Base):
    __tablename__ = 'judgement'

    judgement_id = Column(Integer, primary_key=True)
    solution_id = Column(Integer, ForeignKey('solution.solution_id'))
    testcase_id = Column(Integer, ForeignKey('testcase.testcase_id'))
    verdict = Column(VerdictEnum, nullable=False)
    solved = Column(Boolean)
    runtime = Column(Float)
    memory = Column(Float)

    def get_verdict(self):
        return Verdict[self.verdict]



class SolutionEvent(Base):
    __tablename__ = 'solution_event'

    solution_event_id = Column(Integer, primary_key=True)
    solution_id = Column(Integer, ForeignKey('solution.solution_id'))
    testcase_id = Column(Integer, ForeignKey('testcase.testcase_id'))
    old_status = Column(StatusEnum, nullable=False)
    new_status = Column(StatusEnum, nullable=False)
    event_time = Column(DateTime(timezone=True), nullable=False)


