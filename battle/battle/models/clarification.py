from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from . import Base
from .team import Team


class Clarification(Base):
    __tablename__ = 'clarification'

    clarification_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.team_id'))
    question = Column(String, nullable=False)
    answer = Column(String)
    public = Column(Boolean, nullable=False, default=False)
    question_time = Column(DateTime(timezone=True), nullable=False)
    answer_time = Column(DateTime(timezone=True), nullable=True)

