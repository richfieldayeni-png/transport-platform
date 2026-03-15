import sqlite3

def init():
    conn = sqlite3.connect('transport.db')
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print('Database initialized')

init()
