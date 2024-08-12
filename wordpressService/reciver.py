from pika import BlockingConnection, ConnectionParameters
from rich.console import Console


class reciverWP:
	def __init__(self):
		self.channel = None
		self.connection = None
		self.console = Console()

	def setup(self):
		self.connection = BlockingConnection(ConnectionParameters('localhost'))
		self.channel = self.connection.channel()

	def callback(self,ch, method, properties, body):
		self.console.log(f"Received message: {body}")

	def consume(self):
		self.channel.basic_consume(queue = 'wordpress', on_message_callback = self.callback, auto_ack = True)
		print('Waiting for messages. To exit press CTRL+C')
		self.channel.start_consuming()

	def close(self):
		self.connection.close()


if __name__ == '__main__':
	r = reciverWP()
	r.setup()
	r.consume()
	r.close()
