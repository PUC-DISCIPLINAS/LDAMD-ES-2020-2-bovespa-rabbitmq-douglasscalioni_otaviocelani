import os
import pika

url = os.environ.get('CLOUDAMQP_URL', 'amqps://reprqike:LxlfkjAzqgRfsLIU2_3ZLWnCpaoN4WSb@jackal.rmq.cloudamqp.com/reprqike')
params = pika.URLParameters(url)
params.socket_timeout = 5
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()
