import os
from .base import BaseHandler

class IndexHandler(BaseHandler):

    def get(self):
        with open(os.path.join(os.path.dirname(__file__), '../public/app/index.html'), 'r') as f:
            self.write(f.read())

        # self.template('front/index.html')
