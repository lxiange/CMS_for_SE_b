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
        self.cur.execute("SELECT * FROM announcement WHERE author = '%s'" % author_name)
        res = self.cur.fetchall()
        return res

    def fetch_all_announcement(self):
        self.cur.execute("SELECT * FROM announcement")
        res = self.cur.fetchall()
        return res
#TODO(lxiange): split DaoBase

db = DaoBase('data.db3')

if __name__ == '__main__':
    print(db.fetch_article('root'))
