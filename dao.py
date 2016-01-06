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
        # self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()


class UserDao(DaoBase):
    """docstring for UserDao"""

    def __init__(self, arg):
        super(UserDao, self).__init__(arg)

    def check_pass(self, username, password):
        '''check if user exists
            return None or userinfo.
        '''
        self.cur.execute("SELECT * FROM user WHERE username = ? and password = ?",
                         (username, password))
        res = self.cur.fetchone()
        return res

    def user_exist(self, username):
        '''check if username exists
            return userinfo or None
        '''
        self.cur.execute("SELECT * FROM user WHERE username = ?", (username,))
        res = self.cur.fetchone()
        return res

    def insert(self, *args, **kw):
        '''insert userinfo into table user
            raise exception.
        '''
        try:
            self.cur.execute("INSERT INTO user (username, password, njuid, user_type)"
                             "VALUES (?, ?, ?, ?)", args)
            return True
        except:
            return False
        finally:
            self.conn.commit()


class ArticleDao(DaoBase):
    """docstring for ArticleDao"""

    def __init__(self, arg):
        super(ArticleDao, self).__init__(arg)

    def fetch_all(self):
        '''fetch all articles.
            (use fetchmany())
            return the list of articles.
        '''
        self.cur.execute("SELECT * FROM article")
        res=self.cur.fetchall()
        return res


    def fetch_article(self, author_name):
        '''fetch someone's articles
            return the list of articles.
        '''
        self.cur.execute("SELECT * FROM article WHERE author = '%s'" % author_name)
        res = self.cur.fetchall()
        return res


    def insert(self, *args):
        '''insert an article
            no return.
            raise exceptions.
        '''
        try:
            self.cur.execute("INSERT INTO article (title, author, content, date_, author_id)"
                             "VALUES (?, ?, ?, ?,?)", args)
            return True
        except:
            return False
        finally:
            self.conn.commit()


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

du = UserDao('data.db3')

if __name__ == '__main__':
    print(du.user_exist('sfd'))
    print(du.check_pass('root', 'root'))
    du.insert('12121', '231123', '213123', '2')
