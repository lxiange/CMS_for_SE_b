"""
An operator for operate database
"""
import sqlite3
import time


class DaoBase():
    """docstring for DaoBase"""

    def __init__(self, arg):
        super(DaoBase, self).__init__()
        self.db_name = arg
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
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

    def insert(self, *args):
        '''insert userinfo into table user
            raise exception.
        '''
        assert not self.user_exist(args[0])
        try:
            self.cur.execute("INSERT INTO user (username, password, njuid, user_type)"
                             "VALUES (?, ?, ?, ?)", args)
            return True
        except Exception as e:
            print(e)
            assert 0
            return False
        finally:
            self.conn.commit()

    def fetch(self, username):
        self.cur.execute("SELECT * FROM user WHERE username = ?", (username,))
        res = self.cur.fetchone()
        assert res
        return res

    def fetch_all(self):
        self.cur.execute("SELECT * FROM user")
        res = self.cur.fetchall()
        return res


class UserInfo(DaoBase):
    """docstring for UserInfo"""

    def __init__(self, arg):
        super(UserInfo, self).__init__(arg)

    def insert(self, *args):
        try:
            self.cur.execute("INSERT INTO user_info "
                             "(username, sex, email, birthday, mobile, self_intro)"
                             "VALUES (?, ?, ?, ?, ?, ?)", args)
            return True
        except Exception as e:
            print(e)
            assert 0
            return False
        finally:
            self.conn.commit()

    def fetch(self, username):
        self.cur.execute("SELECT * FROM user_info WHERE username = ?", (username,))
        res = self.cur.fetchone()
        assert res
        return res

    def fetch_all(self):
        self.cur.execute("SELECT * FROM user_info")
        res = self.cur.fetchall()
        return res

    def update(self, username, info_dict):
        try:
            for k, v in info_dict.items():
                print("UPDATE user_info SET %s = %s WHERE username = %s" %
                      (k, v, username))
                self.cur.execute("UPDATE user_info SET {} = ? WHERE username = ?".format(k),
                                 (v, username))
            return True

        except Exception as e:
            print(e)
            assert 0
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
        res = self.cur.fetchall()
        return res

    def fetch_articles(self, author_name):
        '''fetch someone's articles
            return the list of articles.
        '''
        self.cur.execute("SELECT * FROM article WHERE author = ?", (author_name,))
        res = self.cur.fetchall()
        return res

    def insert(self, *args):
        '''insert an article
            no return.
            raise exceptions.
        '''
        try:
            self.cur.execute("INSERT INTO article (title, author, content, date_)"
                             "VALUES (?, ?, ?, ?)", args)
            return True
        except Exception as e:
            print(e)
            assert 0
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

    def fetch_announcement(self, date_):
        '''fetch the announcement of _date
            TODO(lxiange): select announcement by date is useless...
        '''
        self.cur.execute("SELECT * FROM announcement where date_ = ?", (date_,))
        res = self.cur.fetchone()
        return res

    def fetch_all(self):
        '''fetch all articles.
           return the list  of articles.
        '''
        self.cur.execute("SELECT * FROM announcement")
        res = self.cur.fetchall()
        return res

    def insert(self, *args):
        '''insert an Announcement
        '''
        try:
            self.cur.execute("INSERT INTO announcement(title, author, content, date_)"
                             "VALUES (?, ?, ?, ?)", args)
            return True
        except Exception as e:
            print(e)
            assert 0
            return False
        finally:
            self.conn.commit()


class HomeworkDao(DaoBase):
    """for homework itself!"""

    def __init__(self, arg):
        super(HomeworkDao, self).__init__(arg)

    def fetch_by_id(self, homework_id):
        self.cur.execute("SELECT * FROM homework WHERE homework_id=?",
                         (homework_id,))
        res = self.cur.fetchone()
        return res

    def fetch_all(self):
        '''fetch all homework.
           return the list  of homework.
        '''
        self.cur.execute("SELECT * FROM homework")
        res = self.cur.fetchall()
        return res

    def insert(self, *args):
        try:
            self.cur.execute("INSERT INTO homework(title, author, content, date_, deadline)"
                             "VALUES (?, ?, ?, ?, ?)", args)
            return True
        except Exception as e:
            print(e)
            assert 0
            return False
        finally:
            self.conn.commit()


class SubmissionDao(DaoBase):
    """docstring for SubmissionDao"""

    def __init__(self, arg):
        super(SubmissionDao, self).__init__(arg)

    def fetch(self, username):
        '''fetch someone's submission return a list of dict'''
        self.cur.execute("SELECT * FROM submission where author=?", (username,))
        res = self.cur.fetchall()
        return res

    def fetch_by_homework_id(self, homework_id):
        self.cur.execute("SELECT * FROM submission where homework_id = ?",
                         (homework_id,))
        res = self.cur.fetchone()
        return res

    def has_submitted(self, username, homework_id):
        '''someone has submitted the homework'''
        self.cur.execute("SELECT * FROM submission where username = ? and homework_id = ?",
                         (username, homework_id))
        res = self.cur.fetchone()
        if res:
            return True
        else:
            return False

    def insert(self, *args):
        '''add a submit'''
        try:
            self.cur.execute("INSERT INTO submission"
                             "(author, title, content, date_, homework_id, file_path, status)"
                             "VALUES (?, ?, ?, ?, ?, ?, ?)", args)
            return True
        except Exception as e:
            print(e)
            assert 0
            return False
        finally:
            self.conn.commit()


class ResourceDao(DaoBase):
    """docstring for ResourceDao"""

    def __init__(self, arg):
        super(ResourceDao, self).__init__(arg)

    def fetch(self, username):
        '''fetch someone's resources'''


class AdminDao(DaoBase):
    """docstring for AdminDao"""

    def __init__(self, arg):
        super(AdminDao, self).__init__(arg)

    def is_admin(self, username):
        if not username:
            return False
        self.cur.execute(
            "SELECT user_type FROM user WHERE username = ?", (username,))
        res = self.cur.fetchone()
        if res[0] in ['root', 'admin', 'TA']:
            # TODO(lxiange): res['user_type']
            return True
        else:
            return False

    def post_announcement(self, *args, **kw):
        '''post_announcement'''

    def delete_user(self, username):
        '''delete_user'''

    def delete_announcement(self, username):
        '''delete_announcement'''

    def delete_article(self, article_id):
        '''delete_article'''

ud = UserDao('data.db3')
ui = UserInfo('data.db3')
ad = AnnouncementDao('data.db3')
adm = AdminDao('data.db3')
hd = HomeworkDao('data.db3')
sbd = SubmissionDao('data.db3')

if __name__ == '__main__':
    print(ui.fetch_all())
    ui.update('root', {'email': 'fffff@qq.com'})
    print(ui.fetch_all())
    print(adm.is_admin('root'))
