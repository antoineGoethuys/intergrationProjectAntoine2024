import pika

class senderUser:
	def __init__(self):
		self.channel = None
		self.connection = None

	def setup(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel = self.connection.channel()
		self.channel.exchange_declare(
			exchange = 'productData',
			exchange_type = 'fanout',
			durable = True
			)

	def send(self, message):
		self.channel.basic_publish(exchange = 'productData', routing_key = '', body = message)

	def close(self):
		self.connection.close()


if __name__ == '__main__':
	s = senderUser()
	s.setup()
	message = 'Hello, world!user'
	s.send(message)
	s.close()
