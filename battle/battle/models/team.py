from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from battle.api import Role
from . import Base
from .contest import Contest


class Team(Base):
    __tablename__ = 'team'

    team_id = Column(Integer, primary_key=True)
    contest_id = Column(Integer, ForeignKey('contest.contest_id'))
    name = Column(String, nullable=False)

    authors = relationship('Author', backref='team', order_by='Author.author_id')
    testcases = relationship('TestCase', backref='team', order_by='desc(TestCase.submission_time)')
    solutions = relationship('Solution', backref='team', order_by='desc(Solution.submission_time)')
    clarifications = relationship('Clarification', backref='team', order_by='Clarification.clarification_id')


