import signal, sys, sqlite3, os, json

from pika import BlockingConnection, ConnectionParameters
from deepdiff import DeepDiff

from db_setup import create_db

class db:
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
    
    def compare_users(self, user1, user2):
        diff = DeepDiff(user1, user2)
        return diff
        
    def find_user(self, email):
        conn = self.get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return dict(user) if user else None

    def update_user(self, email, new_data):
        conn = self.get_db_connection()
        conn.execute('''
            UPDATE users
            SET username = ?, company = ?, country = ?, postcode = ?, password = ?
            WHERE email = ?
        ''', (new_data['username'], new_data['company'], new_data['country'], new_data['postcode'], new_data['password'], email))
        conn.commit()
        conn.close()
    
    def create_user(self, user_data):
        conn = self.get_db_connection()
        conn.execute('''
            INSERT INTO users (username, email, company, country, postcode, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_data['username'], user_data['email'], user_data['company'], user_data['country'], user_data['postcode'], user_data['password']))
        conn.commit()
        conn.close()
    
    def delete_user(self, email):
        conn = self.get_db_connection()
        conn.execute('DELETE FROM users WHERE email = ?', (email,))
        conn.commit()
        conn.close()

class reciverFOSS:
    def __init__(self):
        create_db()
        self.connection = None
        self.channel = None
        self.db_instance = db()  # Instantiate the db class

    def setup(self):
        self.connection = BlockingConnection(ConnectionParameters('10.0.0.44'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='wordpress', durable=True)
        print("Queue declared and connection established")

    def callback(self, ch, method, properties, body):
        print(f"Received message: {body}")
        message = json.loads(body)
        email = message.get('email')
        action = message.get('action', 'update')  # Default action is 'update'
        
        if action == 'delete':
            self.db_instance.delete_user(email)
            print(f"User deleted: {email}")
        else:
            user = self.db_instance.find_user(email)
            if user:
                print(f"User found: {user}")
                comp = self.db_instance.compare_users(user, message)
                if comp:
                    self.db_instance.update_user(email, message)
                    print(f"User data updated: {message}")
                else:
                    print("No changes detected")
            else:
                self.db_instance.create_user(message)
                print(f"New user created: {message}")
    
    def consume(self):
        print("Starting to consume messages")
        self.channel.basic_consume(queue='wordpress', on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()

def signal_handler(signal, frame):
    r.close()
    sys.exit(0)

if __name__ == '__main__':
    r = reciverFOSS()
    r.setup()
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    r.consume()