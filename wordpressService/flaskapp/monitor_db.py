import time
import sqlite3

def get_last_line(cursor):
    cursor.execute("SELECT * FROM change_log ORDER BY id DESC LIMIT 1")
    return cursor.fetchone()

def monitor_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    last_line = None
    
    while True:
        current_last_line = get_last_line(cursor)
        
        if current_last_line != last_line:
            print(current_last_line)
            last_line = current_last_line
        
        time.sleep(1)  # Check every second

if __name__ == "__main__":
    monitor_table()