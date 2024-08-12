import pika

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a fanout exchange
channel.exchange_declare(exchange = 'userData', exchange_type = 'fanout', durable = True)

# Publish a message to the exchange
message = 'Hello, world!123'
channel.basic_publish(exchange = 'userData', routing_key = '', body = message)

# Close the connection
connection.close()
