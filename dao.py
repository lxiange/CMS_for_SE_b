"""
An operator for operate database
"""
import sqlite3


class DaoBase():
    """docstring for DaoBase"""

    def __init__(self, arg):
        super(DaoBase, self).__init__()
        self.db_name = arg
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def target_in_user(self, target, col_name='username'):
        '''check if target in table user'''
        self.cur.execute("SELECT * FROM user WHERE " +
                         col_name + " = '%s'" % target)
        res = self.cur.fetchall()
        if res:
            return True
        else:
            return False

    def insert_into_user(self, u_name, passwd, njuid, user_type='stu'):
        '''add a new user into table user'''
        # TODO: handle username conflict.
        assert not self.target_in_user(u_name, col_name='username')
        self.cur.execute("INSERT INTO user (username, password, njuid, user_type)\
            VALUES ('%s','%s','%s','%s')" % (u_name, passwd, njuid, user_type))
        self.conn.commit()

    def fetch_user_info(self, username):
        self.cur.execute("SELECT * FROM user WHERE username = '%s'" % username)
        res = self.cur.fetchall()
        assert len(res) <= 1
        return res

    def fetch_article(self, author_name):
        self.cur.execute("SELECT * FROM article WHERE author = '%s'" % author_name)
        res = self.cur.fetchall()
        return res

    def fetch_all_article(self):
        self.cur.execute("SELECT * FROM article")
        res = self.cur.fetchall()
        return res

    def fetch_announcement(self, author_name):
        self.cur.execute(
            "SELECT * FROM announcement WHERE author = '%s'" % author_name)
        res = self.cur.fetchall()
        return res

    def fetch_all_announcement(self):
        self.cur.execute("SELECT * FROM announcement")
        res = self.cur.fetchall()
        return res
# TODO(lxiange): split DaoBase


class UserDao(DaoBase):
    """docstring for UserDao"""

    def __init__(self, arg):
        super(UserDao, self).__init__(arg)

    def check_pass(self, username, password):
        '''check if user exists
            return None or userinfo.
        '''

    def user_exist(self, username):
        '''check if username exists
            return True or False
        '''

    def insert(self, *args, **kw):
        '''insert userinfo into table user
            no return.
            raise exception.
        '''


class ArticleDao(DaoBase):
    """docstring for ArticleDao"""

    def __init__(self, arg):
        super(ArticleDao, self).__init__(arg)

    def fetch_all(self):
        '''fetch all articles.
            (use fetchmany())
            return the list of articles.
        '''

    def fetch_article(self, username):
        '''fetch someone's articles
            return the list of articles.
        '''

    def insert(self, *arg, **kw):
        '''insert an article
            no return.
            raise exceptions.
        '''


class MessageDao(DaoBase):
    """docstring for MessageDao"""

    def __init__(self, arg):
        super(MessageDao, self).__init__(arg)


class AnnouncementDao(DaoBase):
    """docstring for AnnouncementDao"""

    def __init__(self, arg):
        super(AnnouncementDao, self).__init__(arg)


class AdminDao(DaoBase):
    """docstring for AdminDao"""

    def __init__(self, arg):
        super(AdminDao, self).__init__(arg)

    def post_announcement(self, *args, **kw):
        '''post_announcement'''

    def delete_user(self, username):
        '''delete_user'''

    def delete_announcement(self, username):
        '''delete_announcement'''

    def delete_article(self, article_id):
        '''delete_article'''

db = DaoBase('data.db3')
# db = UserDao('data.db3')

if __name__ == '__main__':
    print(db.fetch_article('root'))
