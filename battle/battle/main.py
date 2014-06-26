import tornado
from battle.frontend import application
from battle.backend import daemon

def start_frontend():
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

def start_backend():
    daemon.start()
