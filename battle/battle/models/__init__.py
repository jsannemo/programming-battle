from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Enum

from battle.util.config import config
from battle.api import Status, Language, Verdict, Role

engine = create_engine(config.database)

Base = declarative_base()

StatusEnum = Enum(*Status.get_names(), name='status')
LanguageEnum = Enum(*Language.get_names(), name='language')
VerdictEnum = Enum(*Verdict.get_names(), name='verdict')
RoleEnum = Enum(*Role.get_names(), name='role')

metadata = Base.metadata

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)

from .team import Team
from .contest import Contest
from .problem import Problem
from .submission import TestCase, Solution, SolutionFile, Judgement
from .clarification import Clarification
