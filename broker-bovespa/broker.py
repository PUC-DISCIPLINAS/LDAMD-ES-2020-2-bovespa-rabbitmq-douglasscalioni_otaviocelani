import os
import pika
import sys

# connection
url = os.environ.get('CLOUDAMQP_URL',
                     'amqps://reprqike:LxlfkjAzqgRfsLIU2_3ZLWnCpaoN4WSb@jackal.rmq.cloudamqp.com/reprqike')
params = pika.URLParameters(url)
params.socket_timeout = 5
connection = pika.BlockingConnection(params)

# channel
channel = connection.channel()

# exchange
channel.exchange_declare(exchange='BROKER', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'compra.PTRB'
message = ' '.join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(exchange='BROKER', routing_key=routing_key, body=message)
print(" [x] Sent %r:%r" % (routing_key, message))

connection.close()
