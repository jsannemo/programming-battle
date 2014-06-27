from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from battle.api import Role
from . import Base
from .contest import Contest

class Team(Base):
    __tablename__ = 'team'

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String, nullable=False)
    solver_login = Column(String, nullable=False)
    solver_password = Column(String, nullable=False)
    tester_login = Column(String, nullable=False)
    tester_password = Column(String, nullable=False)
    contest_id = Column(Integer, ForeignKey('contest.contest_id'))

    testcases = relationship('TestCase', backref='team', order_by='desc(TestCase.testcase_time)')
    solutions = relationship('Solution', backref='team', order_by='desc(Solution.solution_time)')


    @staticmethod
    def authenticate(sess, login, password):
        teams = sess.query(Team).from_statement('SELECT * FROM team WHERE'
                '((solver_login = :login AND solver_password = :password) OR (tester_login = :login AND tester_password = :password))'
                'AND contest_id = :contest_id').params(login=login, password=password, contest_id=Contest.get_relevant_contest(sess).contest_id).all()
        if not teams:
            return None
        assert len(teams) == 1, 'Multiple teams with the same login'
        team = teams[0]
        if team.solver_login == login:
            return (team, Role.solver)
        if team.tester_login == login:
            return (team, Role.tester)
        assert false, 'Team matched but is not solver or tester'
