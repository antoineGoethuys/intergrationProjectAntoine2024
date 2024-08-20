import pika
import json

class senderUser:
    def __init__(self):
        self.channel = None
        self.connection = None

    def setup(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
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

        queue_name = 'wordpress'
        try:
            self.channel.queue_declare(queue=queue_name, passive=True)
        except pika.exceptions.ChannelClosedByBroker:
            self.channel = self.connection.channel()  # Reopen the channel
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.queue_bind(exchange='userData', queue=queue_name)
            self.channel.queue_bind(exchange='productData', queue=queue_name)

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


if __name__ == '__main__':
    s = senderUser()
    s.setup()

    # Create the message content
    username = 'antoine.goethuys'
    email = 'antoine.goethuys@student.ehb.bed'
    company = 'EHB'
    country = 'Belgium'
    postcode = '1000'
    password = username + postcode

    # Create message for creating a user
    create_message = {
        'action': 'create',
        'username': username,
        'email': email,
        'company': company,
        'country': country,
        'postcode': postcode,
        'password': password
    }

    # Create message for updating a user
    update_message = {
        'action': 'update',
        'username': username,
        'email': email,
        'company': company,
        'country': country,
        'postcode': postcode+'1',
        'password': password+'1'
    }

    # Create message for deleting a user
    delete_message = {
        'action': 'delete',
        'email': email
    }

    # Convert the messages to JSON
    create_message_json = json.dumps(create_message)
    update_message_json = json.dumps(update_message)
    delete_message_json = json.dumps(delete_message)

    # Send the messages
    # s.send(create_message_json)
    # print(f"Sent create message: {create_message_json}")

    s.send(update_message_json)
    print(f"Sent update message: {update_message_json}")

    # s.send(delete_message_json)
    # print(f"Sent delete message: {delete_message_json}")

    s.close()