import sqlite3

def create_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS users 
              (
               id INTEGER PRIMARY KEY, 
               username TEXT, 
               email TEXT,
               company TEXT,
               country TEXT,
               postcode TEXT,
               password TEXT
              )
              ''')
    c.execute('''
              CREATE TABLE IF NOT EXISTS products 
              (
               id INTEGER PRIMARY KEY, 
               name TEXT,
               price FLOAT
              )
              ''')
    conn.commit()
    conn.close()
if __name__ == '__main__':
    create_db()