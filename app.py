"""Application
This is the app.
"""
import os.path
import random
import sqlite3

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


from handlers import *


class MyApp(tornado.web.Application):
    """docstring for MyApp"""

    def __init__(self):
        handlers = [
            (r'/', indexHandler),
            # (r'/member',memberHandler),
            # (r'/chat/(\d+)',chatHandler),
            (r'/register', registerHandler),
            (r'/logout', logoutHandler),
            (r'/setting/(\w+)', settingHandler),
            (r'/manage', manageHandler),
            (r'/homework/(\w+)', homeworkHandler),
            (r'/submit/(\w+)', submitHomeworkHandler),
            (r'/announcement', announcementHandler),
            # (r'/post',postHandler),
            # (r'/user/(\w+)',userHandler),
            # (r'/blog/(\d+)',blogHandler),
            # (r'/comment',commentHandler),
        ]
        settings = {
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'template_path': os.path.join(os.path.dirname(__file__), 'template'),
            'debug': True,
        }
        super().__init__(handlers, **settings)
        # super().__init__()


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = MyApp()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
