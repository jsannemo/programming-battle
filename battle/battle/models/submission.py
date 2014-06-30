from sqlalchemy import create_engine, Column, Integer, DateTime, String, ForeignKey, Enum, Boolean, Float, CheckConstraint
from sqlalchemy.orm import relationship

from . import Base, StatusEnum, LanguageEnum, VerdictEnum
from battle.api import Language, Status, Verdict



# Testcase:
#     - testcase_id
#     - team_id
#     - problem_id
#     - submission_time
#     - status
#     - contents

class TestCase(Base):
    __tablename__ = 'testcase'

    testcase_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.team_id'))
    problem_id = Column(Integer, ForeignKey('problem.problem_id'))
    submission_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(StatusEnum, nullable=False)
    contents = Column(String, nullable=False)

    # max_judge_time = Column(Float)
    # max_judge_mem = Column(Float)

    def get_status(self):
        return Status[self.status]

    judgements = relationship('Judgement', backref='testcase', order_by='desc(Judgement.judgement_id)')


class Solution(Base):
    __tablename__ = 'solution'

    solution_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.team_id'))
    problem_id = Column(Integer, ForeignKey('problem.problem_id'))
    submission_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(StatusEnum, nullable=False)
    language = Column(LanguageEnum, nullable=False)

    def get_status(self):
        return Status[self.status]

    judgements = relationship('Judgement', backref='solution', order_by='desc(Judgement.judgement_id)')
    files = relationship('SolutionFile', backref='solution', order_by='SolutionFile.file_name')


class SolutionFile(Base):
    __tablename__ = 'solution_file'

    solution_file_id = Column(Integer, primary_key=True)
    solution_id = Column(Integer, ForeignKey('solution.solution_id'))
    file_name = Column(String, nullable=False)
    contents = Column(String, nullable=False)


class Judgement(Base):
    __tablename__ = 'judgement'

    judgement_id = Column(Integer, primary_key=True)
    solution_id = Column(Integer, ForeignKey('solution.solution_id'))
    testcase_id = Column(Integer, ForeignKey('testcase.testcase_id'))
    verdict = Column(VerdictEnum, nullable=False)
    # solved = Column(Boolean) # Do we want this?
    time = Column(Float) # seconds
    memory = Column(Float) # kilobytes
    rejudgement_id = Column(Integer, ForeignKey('judgement.judgement_id'))

    def get_verdict(self):
        return Verdict[self.verdict]

    __table_args__ = (

        # Rejudgement should come later than the judgement itself.
        # This should always be true, but just in case...
        CheckConstraint('rejudgement_id IS NULL OR judgement_id < rejudgement_id'),
    )

