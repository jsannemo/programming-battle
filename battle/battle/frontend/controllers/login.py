import json

from battle.models.team import Team
from .base import BaseHandler


class LoginHandler(BaseHandler):

    def get(self):
        if self.logged_in:
            self.error('You are already logged in')
            return self.redirect('/')
        self.set('login', '')
        self.template('team/login.html')

    def post(self):
        login = self.get_argument('login')
        password = self.get_argument('password')

        team_info = Team.authenticate(self.db, login, password)
        if not team_info:
            self.error('Your login or password is incorrect')
            self.set('login', login)
            self.template('team/login.html')
        else:
            (team, role) = team_info
            if team.contest != self.contest:
                self.error('The team details provided are for another contest')
                self.set('login', login)
                return self.template('team/login.html')
            self.set_cookie_object('team', (team.team_id, role))
            self.redirect('/problems')

class LogoutHandler(BaseHandler):

    def get(self):
        self.set_cookie_object('team', None)
        self.redirect('/')
