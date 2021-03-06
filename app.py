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
            (r'/member', memberHandler),
            (r'/about', aboutHandler),
            # (r'/eggs',eggsHandler),
            (r'/register', registerHandler),        # DONE
            (r'/logout', logoutHandler),            # DONE
            (r'/setting', settingHandler),          # DONE
            (r'/manage/(\w+)', manageHandler),
            (r'/homework/(\w+)', homeworkHandler),
            (r'/submit_homework', submitHomeworkHandler),
            (r'/upload_resource', uploadResourceHandler),
            (r'/announcement', announcementHandler),
            (r'/resource', resourceHandler),
            (r'/download/(\w+)', downloadHandler),
            (r'/message', messageHandler),
            # (r'/user/(\w+)',userHandler),
            (r'/error', errorHandler),              # DONE
            # (r'/post',postHandler),
            # (r'/blog/(\d+)',blogHandler),
            # (r'/comment',commentHandler),
            (r'.*', errorHandler),
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
