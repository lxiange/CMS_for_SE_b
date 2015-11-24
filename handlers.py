import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

class logoutHandler(tornado.web.RequestHandler):
    """docstring for logoutHandler"""

    def get(self):
        self.clear_cookie('hackerName')
        self.redirect('/')


class indexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html', cookieName=self.get_cookie(
            'hackerName'), blogs=[])
    # def post(self):
    #     name = self.get_argument('username')
    #     passwd = self.get_argument('password')
    #     res = self._is_in_db(name)
    #     if res:  # 用户名已存在
    #         self.write('user name comflict')
    #         # self.redirect('/register')
    #     else:
    #         self._insert_into_db(name, passwd)
    #         self.set_cookie('hackerName', name)
    #         # self.write('good!')
    #         self.redirect('/')


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
        assert not self._is_in_db(username)

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
            self.write('user name comflict')
            # self.redirect('/register')
        else:
            self._insert_into_db(name, passwd)
            self.set_cookie('hackerName', name)
            # self.write('good!')
            self.redirect('/')