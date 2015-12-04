''' DB init '''
import sqlite3

db_name = 'data.db3'
conn = sqlite3.connect(db_name)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS\
                 user(user_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                 username VARCHAR(32) UNIQUE,\
                 password VARCHAR(32),\
                 njuid VARCHAR(20),\
                 user_type VARCHAR(32),\
                 e_mail VARCHAR(64))')
cur.execute("INSERT INTO user VALUES (1000,'root','root','131220088','root', NULL)")
