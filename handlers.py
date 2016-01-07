import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from dao import ud
from dao import ui
from dao import ad


class logoutHandler(tornado.web.RequestHandler):
    """docstring for logoutHandler"""

    def get(self):
        self.clear_cookie('stuID')
        self.redirect('/')


class indexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html',
                    cookie_name=self.get_cookie('stuID'),
                    blogs=[],   # TODO(lxiange): use the new dao
                    announcements=ad.fetch_all())

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
            self.redirect('/setting')


class settingHandler(tornado.web.RequestHandler):
    '''edit user infomation'''

    # TODO(lxiange): user photos

    def get(self):
        username = self.get_cookie('stuID')
        if not username:
            self.redirect('error')

        userinfo = ui.fetch(username)
        self.render(
            'setting.html',
            username=userinfo['username'],
            sex=userinfo['sex'],
            user_mail=userinfo['email'],
            birthday=userinfo['birthday'],
            # TODO(lxiange): choose an uniform time format.
            mobile=userinfo['mobile'],
            self_intro=userinfo['self_intro']
        )

    def post(self):
        '''modify'''
        assert self.get_cookie('stuID') == self.get_argument('username')
        ui.update(
            self.get_argument('username'),
            {
                "sex": self.get_argument('sex'),
                "user_mail": self.get_argument('email'),
                "birthday": self.get_argument('birthday'),
                "mobile": self.get_argument('mobile'),
                "self_intro": self.get_argument('self_intro'),
            }
        )
        self.redirect('/')


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
        '''
        http://localhost/announcement/view
        http://localhost/announcement/view?id=
        (admin can edit the announcements)
        '''
        pass

    def post(self):
        '''only admin can post'''
        pass


class homeworkHandler(tornado.web.RequestHandler):
    """assign a homework or view homework"""
    def get(self, para):
        '''
        http://localhost/homework/view
        http://localhost/homework/view?id=
        (admin can download all the homework)

        http://localhost/homework/assign
        (only admin can do that)
        
        '''


class errorHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('error.html')

    def post(self):
        self.redirect('error')
