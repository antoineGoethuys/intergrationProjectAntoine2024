from pika import BlockingConnection, ConnectionParameters
from rich.console import Console

class reciverFOSS:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.console = Console()

    def setup(self):
        self.console.log("Setting up connection and channel...")
        self.connection = BlockingConnection(ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.console.log("Connection and channel established.")

    def callback(self, ch, method, properties, body):
        self.console.log(f"Received message: {body}")

    def consume(self):
        self.console.log("Starting to consume messages...")
        self.channel.basic_consume(queue='FOSSbilling', on_message_callback=self.callback, auto_ack=True)
        self.console.log('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.console.log("Closing connection...")
        self.connection.close()
        self.console.log("Connection closed.")

if __name__ == '__main__':
    r = reciverFOSS()
    r.setup()
    try:
        r.consume()
    except KeyboardInterrupt:
        r.close()