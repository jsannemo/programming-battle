import pickle
import tornado.web

from battle.models import Session, Contest, Author, Problem

class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        self.db = Session()
        self._template_arguments = {}
        self.contest = Contest.get_relevant_contest(self.db)
        self.logged_in = self.get_cookie_object('author')

        if self.logged_in:
            author_id = self.logged_in
            author = self.db.query(Author).get(author_id)
            if author:
                self.author = author
                self.author_id = author.author_id
                self.team_id = author.team_id
                self.set('author', self.author)
            else:
                self.logged_in = False
        self.set('logged_in', True if self.logged_in else False)

        self.set('contest', self.contest)
        self.set('errors', self.get_cookie_object('errors') or [])

    def set(self, key, val):
        self._template_arguments[key] = val

    def template(self, template_name):
        self.set_cookie_object('errors', [])
        self.render(template_name, **self._template_arguments)

    def on_finish(self):
        self.db.close()

    def error(self, message):
        self._template_arguments['errors'].append(message)
        self.set_cookie_object('errors', self._template_arguments['errors'])

    def set_cookie_object(self, name, obj):
        self.set_secure_cookie(name, pickle.dumps(obj))

    def get_cookie_object(self, name):
        cookie = self.get_secure_cookie(name)
        if cookie:
            return pickle.loads(self.get_secure_cookie(name))
        return None

    def die(self, msg):
        # TODO better error page
        self.write(msg)

def valid_problem(func):
    def wrap(self, *args, **kwargs):
        problem_tag = self.path_kwargs['problem_tag']
        sess = self.db
        problems = Problem.find_by_tag(sess, problem_tag)

        if len(problems) == 0:
            self.error('Invalid problem')
            return self.redirect('/')

        problem = problems[0]
        if problem.contest != self.contest:
            self.error('Invalid problem')
            return self.redirect('/')

        if problem.available_from >= self.contest.get_elapsed():
            self.error('Invalid problem')
            return self.redirect('/')

        return func(self, *args, **kwargs)
    return wrap

def require_login(func):
    def wrap(self, *args, **kwargs):
        if not self.logged_in:
            self.error('This page requires you to be logged in')
            self.redirect('/')
        else:
            return func(self, *args, **kwargs)
    return wrap

