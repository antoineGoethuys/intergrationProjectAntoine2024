import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


def callback(ch, method, properties, body):
	print(f"Received message: {body}")


channel.basic_consume(queue = 'FOSSbilling', on_message_callback = callback, auto_ack = True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

connection.close()
