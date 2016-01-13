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
cur.execute("INSERT INTO user VALUES (1000,'lxiange','lxiange','131220088','stu')")


cur.execute("CREATE TABLE article(\
                article_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                title VARCHAR(512),\
                author VARCHAR(100),\
                content VARCHAR(1000000),\
                date_ VARCHAR(100))")
cur.execute("INSERT INTO article \
    VALUES (1000,'hello world','root','Hello! It is  a test!','2016-01-08 23:57:32')")


cur.execute("CREATE TABLE announcement(\
                announcement_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                title VARCHAR(512),\
                author VARCHAR(100),\
                content VARCHAR(1000000),\
                date_ VARCHAR(100))")
cur.execute("INSERT INTO announcement \
    VALUES (1000,'announcement title','root','Hello! It is  a test!','2016-01-08 23:57:32')")


cur.execute("CREATE TABLE user_info (\
                username VARCHAR(32),\
                sex VARCHAR(16),\
                email VARCHAR(128),\
                truename VARCHAR(128),\
                mobile VARCHAR(20),\
                self_intro VARCHAR(100000))")
cur.execute("INSERT INTO user_info VALUES (?, ?, ?, ?, ?, ?)",
            ('root', 'male', 'root@root.com', '2009-11-1', '13425243343', 'hello world!'))


cur.execute("CREATE TABLE homework (\
                homework_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                title VARCHAR(512),\
                author VARCHAR(100),\
                content VARCHAR(1000000),\
                date_ VARCHAR(100),\
                deadline VARCHAR(100))")
cur.execute("INSERT INTO homework VALUES (?, ?, ?, ?, ?, ?)",
            (1000, 'eat shit', 'root', 'ffffffff', '2013-01-08 23:57:32', '2016-01-18 23:57:32'))


cur.execute("CREATE TABLE submission (\
                submission_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                author VARCHAR(128),\
                title VARCHAR(512),\
                content VARCHAR(1000000),\
                date_ VARCHAR(100),\
                homework_id INTEGER,\
                file_path VARCHAR(500),\
                status VARCHAR(100))")
cur.execute("INSERT INTO submission VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (1000, 'root', 'first commit', 'this is the content', '2013-01-08 23:57:32', 1000, '/homework/1/111.rar', 'submitted'))

cur.execute("CREATE TABLE resource (\
                resource_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                author VARCHAR(128),\
                title VARCHAR(512),\
                content VARCHAR(1000000),\
                date_ VARCHAR(100),\
                file_path VARCHAR(500))")
cur.execute("INSERT INTO resource VALUES (?, ?, ?, ?, ?, ?)",
            (1000, 'root', 'first resource', 'this is the first resource', '2013-01-08 23:57:32', ''))


conn.commit()
conn.close()

try:
    os.mkdir('data')
except:
    pass

try:
    os.mkdir('data/user_pic')
except:
    pass

try:
    os.mkdir('data/resource')
except:
    pass

try:
    os.mkdir('data/homework')
except:
    pass

try:
    os.mkdir('data/homework/hw_1000')
except:
    pass
