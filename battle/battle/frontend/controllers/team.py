from .base import BaseHandler

from battle.models import Team

class TeamViewHandler(BaseHandler):

    def get(self, team_id=None):
        if team_id == None:
            if not self.logged_in:
                self.error('You must be logged in to view your team page')
                self.redirect("/")
                return
            team_id = self.author.team.team_id
        try:
            team_id = int(team_id)
        except:
            self.error('Invalid team')
            return self.redirect("/")
        team = self.db.query(Team).get(team_id)
        if not team or team.contest != self.contest:
            self.error("Invalid team")
            self.redirect("/")
            return

        self.set('view_team', team)
        self.template('team/view.html')

