import pika


class senderProduct:
	def __init__(self):
		self.channel = None
		self.connection = None

	def setup(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel = self.connection.channel()
		self.channel.exchange_declare(
			exchange = 'userData',
			exchange_type = 'fanout',
			durable = True
			)

	def send(self, message):
		# Publish a message to the exchange
		self.channel.basic_publish(exchange = 'userData', routing_key = '', body = message)

	def close(self):
		# Close the connection
		self.connection.close()

if __name__ == '__main__':
	s = senderProduct()
	s.setup()
	message = 'Hello, world!product'
	s.send(message)
	s.close()
