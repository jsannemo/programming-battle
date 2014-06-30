from sqlalchemy import Column, Integer, String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from . import Base, RoleEnum
from .team import Team
from battle.api import Role

class Author(Base):
    __tablename__ = 'author'

    author_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.team_id'))
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(RoleEnum, nullable=False)

    def get_role(self):
        return Role[self.role]

    @staticmethod
    def authenticate(sess, username, password):
        return sess.query(Author).from_statement(
                'SELECT * FROM author WHERE '
                'username = :username AND password = :password '
            ).params(username=username, password=password).first()

