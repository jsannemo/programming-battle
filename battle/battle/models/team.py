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
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    testcases = relationship('TestCase', backref='team', order_by='desc(TestCase.submission_time)')
    solutions = relationship('Solution', backref='team', order_by='desc(Solution.submission_time)')
    clarifications = relationship('Clarification', backref='team', order_by='Clarification.clarification_id')

    @staticmethod
    def authenticate(sess, username, password):
        print(username)
        print(password)
        team = sess.query(Team).from_statement("SELECT * from team WHERE username = :username AND password = :password").params({'username': username, 'password': password}).all()
        if team:
            return team[0]
        return None
