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
        self.cur.execute('CREATE TABLE IF NOT EXISTS\
                         user(user_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                         username VARCHAR(32) UNIQUE,\
                         password VARCHAR(32),\
                         njuid VARCHAR(20),\
                         user_type VARCHAR(32),\
                         e_mail VARCHAR(64))')
        self.cur.execute("INSERT INTO user \
            VALUES (1000,'root','root','131220088','root', NULL)")

        # TODO: if db has existed do not insert.

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


db = DaoBase('data.db3')
