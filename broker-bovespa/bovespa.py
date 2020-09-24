import pika
import os
import sys

# connection
server = sys.argv[1] if len(sys.argv) > 1 else 'amqps://reprqike:LxlfkjAzqgRfsLIU2_3ZLWnCpaoN4WSb@jackal.rmq.cloudamqp.com/reprqike'
url = os.environ.get('CLOUDAMQP_URL',
                     server)
params = pika.URLParameters(url)
params.socket_timeout = 5
connection = pika.BlockingConnection(params)

# channel
channel = connection.channel()

# exchange
channel.exchange_declare(exchange='BROKER', exchange_type='topic')

# queues
channel.queue_declare(queue='ordens_venda', exclusive=True)
channel.queue_declare(queue='ordens_compra', exclusive=True)

'''binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)'''

channel.queue_bind(exchange='BROKER', queue='ordens_venda', routing_key='venda.*')
channel.queue_bind(exchange='BROKER', queue='ordens_compra', routing_key='compra.*')


print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(queue='ordens_venda', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue='ordens_compra', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
