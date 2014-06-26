from datetime import datetime
import pytz

from sqlalchemy import Column, Integer, DateTime, Interval, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class MultipleContestsError(Exception):
    pass

class NoContestError(Exception):
    pass

class Contest(Base):
    __tablename__ = 'contest'

    contest_id = Column(Integer, primary_key=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    length = Column(Interval, nullable=False)
    name = Column(String, nullable=False)
    tag = Column(String, nullable=False, unique=True)

    teams = relationship('Team', order_by='Team.team_id', backref='contest')
    problems = relationship('Problem', order_by='Problem.contest_order', backref='contest')

    def is_started(self):
        now = datetime.now(pytz.utc)
        return now >= self.start_time

    def is_running(self):
        now = datetime.now(pytz.utc)
        return self.is_started() and now <= self.get_end_time()

    def is_finished(self):
        return self.is_started() and not self.is_running()

    def get_end_time(self):
        return self.start_time + self.length

    @staticmethod
    def get_current_contest(sess):
        contests = sess.query(Contest).from_statement("SELECT * FROM contest WHERE start_time <= now() AND start_time + length >= now()").all()
        if len(contests) == 0:
            return None
        if len(contests) > 1:
            raise MultipleContestsError
        return contests[0]

    @staticmethod
    def get_next_contest(sess):
        contests = sess.query(Contest).from_statement("SELECT * FROM contest WHERE start_time >= now() ORDER BY start_time ASC LIMIT 1").all()
        if contests:
            return contests[0]
        return None

    @staticmethod
    def get_past_contest(sess):
        contests = sess.query(Contest).from_statement("SELECT * from contest WHERE start_time + length < now() ORDER BY start_time + length DESC LIMIT 1").all()
        if contests:
            return contests[0]
        return

    @staticmethod
    def get_relevant_contest(sess):
        current = Contest.get_current_contest(sess)
        if current:
            return current
        next = Contest.get_next_contest(sess)
        if next:
            return next
        past = Contest.get_next_contest(sess)
        if past:
            return past
        raise NoContestError
