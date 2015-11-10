"""Application
This is the app.
"""
import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import sqlite3

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class MyApp(tornado.web.Application):
    """docstring for MyApp"""

    def __init__(self):
        handlers = [
            (r'/', indexHandler),
            # (r'/member',memberHandler),
            # (r'/chat/(\d+)',chatHandler),
            (r'/register', registerHandler),
            # (r'/logout',logoutHandler),
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


class indexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class registerHandler(tornado.web.RequestHandler):
    """Doc:
    handle regist information
    """

    def __init__(self, *args, **kwargs):
        super(registerHandler, self).__init__(*args, **kwargs)
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS\
                         user(username VARCHAR(20) UNIQUE,\
                         password VARCHAR(32),\
                         user_type VARCHAR(32))')

    def _is_in_db(self, username):
        '''check if username in table user'''
        self.cur.execute("SELECT * FROM user WHERE username = '%s'" % username)
        res = self.cur.fetchall()
        if res:
            return True
        else:
            return False

    def _insert_into_db(self, username, passwd, user_type='stu'):
        '''Insert user to db'''
        assert self._is_in_db(username)

        self.cur.execute("INSERT INTO user VALUES ('%s','%s','%s')" %
                         (username, passwd, user_type))
        self.conn.commit()

    def get(self):
        self.render('register.html')

    def post(self):
        name = self.get_argument('username')
        passwd = self.get_argument('password')
        res = self._is_in_db(name)
        if res:  # 用户名已存在
            self.redirect('/register')
        else:
            self._insert_into_db(name, passwd)
            self.set_cookie('hackerName', name)
            self.redirect('/')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = MyApp()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
