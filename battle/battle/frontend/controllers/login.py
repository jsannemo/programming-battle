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
        username = self.get_argument('login')
        password = self.get_argument('password')

        team = Team.authenticate(self.db, username, password)
        if not team:
            self.error('Your login or password is incorrect')
            self.set('login', username)
            self.template('team/login.html')
        else:
            # if team.contest != self.contest:
            #     self.error('The team details provided are for another contest')
            #     self.set('login', login)
            #     return self.template('team/login.html')
            self.set_cookie_object('team', team.team_id)
            self.redirect('/problems')

class LogoutHandler(BaseHandler):

    def get(self):
        self.set_cookie_object('team', None)
        self.redirect('/')
