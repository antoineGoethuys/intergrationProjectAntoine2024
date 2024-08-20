import json, os, time, requests, pika, sqlite3

from deepdiff import DeepDiff
from requests.auth import HTTPBasicAuth
from rich import print

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

class senderUser:
    def __init__(self):
        self.channel = None
        self.connection = None

    def setup(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='10.0.0.44',  # Replace with the actual IP address of the RabbitMQ server
            port=5672,  # Default RabbitMQ port
            credentials=pika.PlainCredentials('guest', 'guest')  # Update with your RabbitMQ credentials
        ))
        self.channel = self.connection.channel()

    def send(self, message):
        self.channel.basic_publish(
            exchange='userData',
            routing_key='',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

    def close(self):
        self.connection.close()

class ChangeDetector:
 def __init__(self):
  create_db()
  self.connection = None
  self.channel = None
 def get_db_connection(self):
  if not os.path.exists('data.db'):
   create_db()
  conn = sqlite3.connect('data.db')
  conn.row_factory = sqlite3.Row
  return conn
 def get_user_by_id(self, user_id):
  conn = self.get_db_connection()
  user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
  conn.close()
  return dict(user) if user else None
 def get_last_change(self):
  conn = self.get_db_connection()
  last_change = conn.execute('SELECT * FROM change_log ORDER BY id DESC LIMIT 1').fetchone()
  conn.close()
  return dict(last_change) if last_change else None
 def transform_into_user(self, operation, user):
  if operation == 'UPDATE':
   return self.get_user_by_id(user['row_id'])
  if operation == 'INSERT':
   return self.get_user_by_id(user['row_id'])
  if operation == 'DELETE':
   return self.get_user_by_id(user['row_id'])
 def transform_into_message(self, operation, user_data):
  action_map = {
   'INSERT': 'add',
   'UPDATE': 'update',
   'DELETE': 'delete'
  }
  return {
   'action': action_map.get(operation, 'unknown'),
   'username': user_data['username'],
   'email': user_data['email'],
   'company': user_data['company'],
   'country': user_data['country'],
   'postcode': user_data['postcode'],
   'password': user_data['password']
  }

if __name__ == '__main__':
 sender = senderUser()
 sender.setup()
 change_detector = ChangeDetector()
 last_sent_message = None
 while True:
  last = change_detector.get_last_change()
  print(f'last{last}')
  time.sleep(5)
  last1 = change_detector.get_last_change()
  print(f'last1{last1}')
  if last != last1:
   user = change_detector.transform_into_user(last1['operation'], last1)
   message = change_detector.transform_into_message(last1['operation'], user)
   sender.send(json.dumps(message))
  
 sender.close()