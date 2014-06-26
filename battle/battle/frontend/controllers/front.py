from .base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        self.template('front/index.html')
