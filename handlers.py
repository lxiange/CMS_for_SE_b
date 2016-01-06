import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from dao import ud
from dao import ui


class logoutHandler(tornado.web.RequestHandler):
    """docstring for logoutHandler"""

    def get(self):
        self.clear_cookie('stuID')
        self.redirect('/')


class indexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html', cookieName=self.get_cookie('stuID'),
                    blogs=[],   # TODO(lxiange): use the new dao
                    announcements=[])

    def post(self):
        '''login'''
        name = self.get_argument('username')
        password = self.get_argument('password')
        res = ud.check_pass(name, password)
        if res:
            self.set_cookie('stuID', name)
            self.redirect('/')
        else:
            pass
            # TODO(lxiange): wrong password



class registerHandler(tornado.web.RequestHandler):
    """Doc:
    handle regist information
    """

    def get(self):
        self.render('register.html', same_name=False)

    def post(self):
        name = self.get_argument('username')
        password = self.get_argument('password')
        njuid = self.get_argument('njuid')

        res = ud.user_exist(name)
        if res:  # user exists
            self.render('/register', same_name=True)
        else:
            ud.insert(name, password, njuid, 'stu')
            ui.insert(name, '', '', '', '')
            self.set_cookie('stuID', name)
            self.redirect('/setting/info')


class settingHandler(tornado.web.RequestHandler):
    '''edit user infomation and modify the password'''
    def get(self):
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('error')

        userinfo = ui.fetch(username)
        self.render('setting.html', userMail=userinfo['email'], cookieName=userinfo[1],
                    sex=None, birthday=None, city=None, intro=None)# TODO(lxiange): modify it
        # elif para == 'pw':
        #     self.render('pw.html', cookieName=username, sameOldPw=True)

    def post(self):
        '''modify'''


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


class errorHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('error.html')