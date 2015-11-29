import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from dao import db


class logoutHandler(tornado.web.RequestHandler):
    """docstring for logoutHandler"""

    def get(self):
        self.clear_cookie('stuID')
        self.redirect('/')


class indexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html', cookieName=self.get_cookie(
            'stuID'), blogs=[])
    # def post(self):
    #     name = self.get_argument('username')
    #     passwd = self.get_argument('password')
    #     res = self._is_in_db(name)
    #     if res:  # 用户名已存在
    #         self.write('user name comflict')
    #         # self.redirect('/register')
    #     else:
    #         self._insert_into_db(name, passwd)
    #         self.set_cookie('stuID', name)
    #         # self.write('good!')
    #         self.redirect('/')


class registerHandler(tornado.web.RequestHandler):
    """Doc:
    handle regist information
    """



    def get(self):
        self.render('register.html')

    def post(self):
        name = self.get_argument('username')
        passwd = self.get_argument('password')
        njuid=self.get_argument('njuid')
        res = db.target_in_user(name,'username')
        if res:  # 用户名已存在
            self.write('user name comflict')
            # self.redirect('/register')
        else:
            db.insert_into_user(name, passwd,njuid)
            self.set_cookie('stuID', name)
            # self.write('good!')
            self.redirect('/')
