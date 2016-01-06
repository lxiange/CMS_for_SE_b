''' DB init '''
import sqlite3
import os

db_name = 'data.db3'
try:
    os.remove(db_name)
except:
    pass
conn = sqlite3.connect(db_name)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS\
                 user(\
                 user_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                 username VARCHAR(32) UNIQUE,\
                 password VARCHAR(32),\
                 njuid VARCHAR(20),\
                 user_type VARCHAR(32))')
cur.execute("INSERT INTO user VALUES (1000,'root','root','131220088','root')")

cur.execute("CREATE TABLE article(\
                article_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                title VARCHAR(512),\
                author VARCHAR(100),\
                content VARCHAR(1000000),\
                date_ VARCHAR(100),\
                author_id INTEGER)")
cur.execute("INSERT INTO article \
    VALUES (1000,'hello world','root','Hello! It is  a test!','fuck_time', 1000)")

cur.execute("CREATE TABLE announcement(\
                announcement_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                title VARCHAR(512),\
                author VARCHAR(100),\
                content VARCHAR(1000000),\
                date_ VARCHAR(100),\
                author_id INTEGER)")

cur.execute("INSERT INTO announcement \
    VALUES (1000,'announcement title','root','Hello! It is  a test!','fuck_time', 1000)")

# todo : create table user detail infomation
cur.execute("CREATE TABLE user_info (\
                username VARCHAR(32),\
                sex VARCHAR(16),\
                e_mail VARCHAR(128),\
                birthday VARCHAR(128),\
                mobile VARCHAR(20),\
                self_intro VARCHAR(100000))")

conn.commit()
conn.close()
