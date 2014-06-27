import tornado.web

from .controllers.front import IndexHandler
from .controllers.login import LoginHandler, LogoutHandler
from .controllers.problem import ProblemListHandler, ProblemViewHandler
from .controllers.submission import SubmitHandler, SolutionViewHandler, SolutionDownloadHandler, SolutionListHandler, TestcaseViewHandler, TestcaseDownloadHandler, TestcaseListHandler
from .controllers.team import TeamViewHandler
from .controllers.standings import StandingsHandler

from battle.util.config import config

application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/problems', ProblemListHandler),
    (r'/problem/(?P<problem_tag>[^/]+)', ProblemViewHandler),
    (r'/problem/(?P<problem_tag>[^/]+)/submit', SubmitHandler),
    (r'/problem/(?P<problem_tag>[^/]+)/solutions', SolutionListHandler),
    (r'/problem/(?P<problem_tag>[^/]+)/testcases', TestcaseListHandler),
    (r'/solution/(?P<solution_id>[^/]+)', SolutionViewHandler),
    (r'/testcase/(?P<testcase_id>[^/]+)', TestcaseViewHandler),
    (r'/download/solution/(?P<solution_id>[^/]+)', SolutionDownloadHandler),
    (r'/download/testcase/(?P<testcase_id>[^/]+)', TestcaseDownloadHandler),
    (r'/team/(?P<team_id>[^/]+)', TeamViewHandler),
    (r'/team', TeamViewHandler),
    (r'/standings', StandingsHandler),
],**config.web_config)


__all__ = ['application', 'BaseHandler']
