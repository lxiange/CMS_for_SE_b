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
        self.render('index.html', cookieName=self.get_cookie('stuID'),
                    blogs=db.fetch_all_article(),
                    announcements=db.fetch_all_announcement())

    def post(self):
        '''login'''
        name = self.get_argument('username')
        passwd = self.get_argument('password')
        # res = self.target_in_user(name)
        # if res:  # 用户名已存在
        #     self.write('user name comflict')
        #     # self.redirect('/register')
        # else:
        #     self._insert_into_db(name, passwd)
        #     self.set_cookie('stuID', name)
        #     # self.write('good!')
        #     self.redirect('/')


class registerHandler(tornado.web.RequestHandler):
    """Doc:
    handle regist information
    """

    def get(self):
        self.render('register.html', sameName=False, sameMail=False)

    def post(self):
        name = self.get_argument('username')
        passwd = self.get_argument('password')
        njuid = self.get_argument('njuid')

        res = db.target_in_user(name, 'username')
        if res:  # 用户名已存在
            self.write('user name comflict')
            # TODO(lxiange): redirect
            # self.redirect('/register')
        else:
            db.insert_into_user(name, passwd, njuid)
            self.set_cookie('stuID', name)
            self.redirect('/setting/info')


class settingHandler(tornado.web.RequestHandler):
    '''edit user infomation and modify the password'''
    def get(self, para):
        username = self.get_cookie('stuID')
        userinfo = db.fetch_user_info(username)[0]

        if para == 'info':
            self.render('setting.html', userMail=userinfo[5], cookieName=userinfo[1],
                        sex=None, birthday=None, city=None, intro=None)
        # elif para == 'pw':
        #     self.render('pw.html', cookieName=username, sameOldPw=True)


class manageHandler(tornado.web.RequestHandler):
    '''handler for admin to manage'''

    def get(self):
        pass


class submitHomeworkHandler(tornado.web.RequestHandler):
    '''handler for submit homework'''

    def get(self):
        pass

    def post(self):
        pass


class announcementHandler(tornado.web.RequestHandler):
    '''post an announcement, only admin can do this'''
    def get(self):
        pass
        
    def post(self):
        pass

class homeworkHandler(tornado.web.RequestHandler):
     """assign a homework or view homework"""
