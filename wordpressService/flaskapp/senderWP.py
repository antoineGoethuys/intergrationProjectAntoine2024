import signal, sys, sqlite3, os, json, pika

from pika import BlockingConnection, ConnectionParameters
from deepdiff import DeepDiff

from db_setup import create_db


class senderUser:
    def __init__(self):
        self.channel = None
        self.connection = None

    def setup(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost',  # Update with your RabbitMQ host
            port=5672,  # Default RabbitMQ port
            credentials=pika.PlainCredentials('guest', 'guest')  # Update with your RabbitMQ credentials
        ))
        self.channel = self.connection.channel()

        # Declare the exchanges
        self.channel.exchange_declare(
            exchange='userData',
            exchange_type='fanout',
            durable=True
        )
        self.channel.exchange_declare(
            exchange='productData',
            exchange_type='fanout',
            durable=True
        )

        # Declare the queues
        self.channel.queue_declare(queue='FOSSbilling', durable=True)
        self.channel.queue_declare(queue='wordpress', durable=True)

        # Bind the queues to the exchanges
        self.channel.queue_bind(exchange='userData', queue='FOSSbilling')
        self.channel.queue_bind(exchange='userData', queue='wordpress')
        self.channel.queue_bind(exchange='productData', queue='FOSSbilling')
        self.channel.queue_bind(exchange='productData', queue='wordpress')

    def send(self, message, exchange):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key='',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

    def close(self):
        self.connection.close()

# class ChangeDetector:
#     def __init__(self):
#         create_db()
#         self.connection = None
#         self.channel = None

#     def get_db_connection(self):
#         if not os.path.exists('data.db'):
#             create_db()
#         conn = sqlite3.connect('data.db')
#         conn.row_factory = sqlite3.Row
#         return conn

#     def get_user_by_id(self, user_id):
#         conn = self.get_db_connection()
#         user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
#         conn.close()
#         return dict(user) if user else None

#     def get_last_change(self):
#         conn = self.get_db_connection()
#         last_change = conn.execute('SELECT * FROM change_log').fetchone()
#         conn.close()
#         return dict(last_change) if last_change else None

#     def transform_into_user(self, operation, user):
#         if operation == 'UPDATE':
#             return self.get_user_by_id(user['row_id'])
#         if operation == 'INSERT':
#             return self.get_user_by_id(user['row_id'])
#         if operation == 'DELETE':
#             return self.get_user_by_id(user['row_id'])

#     def transform_into_message(self, operation, user_data):
#         action_map = {
#             'INSERT': 'add',
#             'UPDATE': 'update',
#             'DELETE': 'delete'
#         }
#         return {
#             'action': action_map.get(operation, 'unknown'),
#             'username': user_data['username'],
#             'email': user_data['email'],
#             'company': user_data['company'],
#             'country': user_data['country'],
#             'postcode': user_data['postcode'],
#             'password': user_data['password']
#         }


if __name__ == '__main__':
 sender = senderUser()
 sender.setup()
 message = "Hello, RabbitMQ!"
 sender.send(message, 'userData')
 sender.send(message, 'productData')
 sender.close()
    # s = senderUser()
    # s.setup()
    # s.send('Hello World')
    # # change_detector = ChangeDetector()
    # # last_change = change_detector.get_last_change()
    # # if last_change:
    # #     user_details = change_detector.transform_into_user(last_change['operation'], last_change)
    # #     if user_details:
    # #         message = change_detector.transform_into_message(last_change['operation'], user_details)
    # #         user_json = json.dumps(message)
    # #         s.send(user_json)
    # s.close()
    # # # Create the message content
    # # username = 'antoine.goethuys'
    # # email = 'antoine.goethuys@student.ehb.bed'
    # # company = 'EHB'
    # # country = 'Belgium'
    # # postcode = '1000'
    # # password = username + postcode

    # # # Create message for creating a user
    # # create_message = {
    # #     'action': 'create',
    # #     'username': username,
    # #     'email': email,
    # #     'company': company,
    # #     'country': country,
    # #     'postcode': postcode,
    # #     'password': password
    # # }

    # # # Create message for updating a user
    # # update_message = {
    # #     'action': 'update',
    # #     'username': username,
    # #     'email': email,
    # #     'company': company,
    # #     'country': country,
    # #     'postcode': postcode+'1',
    # #     'password': password+'1'
    # # }

    # # # Create message for deleting a user
    # # delete_message = {
    # #     'action': 'delete',
    # #     'email': email
    # # }

    # # # Convert the messages to JSON
    # # create_message_json = json.dumps(create_message)
    # # update_message_json = json.dumps(update_message)
    # # delete_message_json = json.dumps(delete_message)

    # # # Send the messages
    # # # s.send(create_message_json)
    # # # print(f"Sent create message: {create_message_json}")

    # # s.send(update_message_json)
    # # print(f"Sent update message: {update_message_json}")

    # # # s.send(delete_message_json)
    # # # print(f"Sent delete message: {delete_message_json}")