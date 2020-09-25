import os
import pika
import sys

from LivroDeOfertas import LivroDeOfertas


def main():
    # connection
    url = os.environ.get('CLOUDAMQP_URL',
                         'amqps://reprqike:LxlfkjAzqgRfsLIU2_3ZLWnCpaoN4WSb@jackal.rmq.cloudamqp.com/reprqike')
    params = pika.URLParameters(url)
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params)

    # channel
    broker_channel = connection.channel()
    bolsa_channel = connection.channel()

    # exchange
    broker_channel.exchange_declare(exchange='BROKER', exchange_type='topic')
    bolsa_channel.exchange_declare(
        exchange='BOLSADEVALORES', exchange_type='topic')

    # publish
    routing_key = sys.argv[1] if len(sys.argv) > 2 else 'compra.PTRB'
    message = ' '.join(sys.argv[1:]) or "info: Hello World!"

    broker_channel.basic_publish(
        exchange='BROKER', routing_key=routing_key, body=message)
    print(" [x] Sent %r:%r" % (routing_key, message))
    # print("binding k: " + binding_key)

    # consume
    receive = bolsa_channel.queue_declare(queue='', exclusive=True)
    queue_name = receive.method.queue  # gets queue (random) name

    # substituir por um arquivo depois (BINDING KEYS PERTINENTES)
    binding_keys = sys.argv[2:]
    bolsa_channel.queue_bind(exchange='BOLSADEVALORES',
                             queue=queue_name, routing_key='*.*')

    ofertas = LivroDeOfertas()

    def callback(ch, method, properties, body):
        if method.routing_key.split('.')[0] == 'transacao':
            ofertas.update_transaction(method.routing_key, body)
        else:
            ofertas.new_ordem(method.routing_key, body)
        print(" [x] %r:%r" % (method.routing_key, body))

    bolsa_channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    bolsa_channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
