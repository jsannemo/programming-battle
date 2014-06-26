import json

from battle.models.team import Team
from .base import BaseHandler


class LoginHandler(BaseHandler):


    # TODO check if is logged in
    def get(self):
        self.set('login', '')
        self.template('team/login.html')

    def post(self):
        login = self.get_argument('login')
        password = self.get_argument('password')

        # TODO check if the team contest is the same as the current(/next) one
        team_info = Team.authenticate(self.db, login, password)
        if not team_info:
            self.error('Your login or password is incorrect')
            self.set('login', login)
            self.template('team/login.html')
        else:
            (team, role) = team_info
            # TODO success message
            self.set_cookie_object('team', (team.team_id, role))
            self.redirect('/problems')

class LogoutHandler(BaseHandler):

    # TODO add success message
    def get(self):
        self.set_cookie_object('team', None)
        self.redirect('/')
