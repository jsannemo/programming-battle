from .base import BaseHandler

from battle.models import Team

class TeamViewHandler(BaseHandler):

    def get(self, team_id=None):
        if team_id == None:
            if not self.logged_in:
                self.error('You must be logged in to view your team page')
                self.redirect("/")
                return
            team_id = self.team.team_id
        team = self.db.query(Team).get(team_id)
        if not team:
            self.error("Invalid team")
            self.redirect("/")
            return

        self.set('view_team', team)
        self.template('team/view.html')

