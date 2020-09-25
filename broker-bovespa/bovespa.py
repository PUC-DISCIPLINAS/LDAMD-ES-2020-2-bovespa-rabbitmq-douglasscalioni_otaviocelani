import pika
import os
import sys


class Ordem:
    def __init__(self, tipo, ativo, quant, val, broker):
        self.tipo = tipo
        self.ativo = ativo
        self.quant = quant
        self.val = val
        self.broker = broker


def main():
    # connection
    server = sys.argv[1] if len(
        sys.argv) > 1 else 'amqps://reprqike:LxlfkjAzqgRfsLIU2_3ZLWnCpaoN4WSb@jackal.rmq.cloudamqp.com/reprqike'
    url = os.environ.get('CLOUDAMQP_URL',
                         server)
    params = pika.URLParameters(url)
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params)

    # channel
    broker_channel = connection.channel()
    bolsa_channel = connection.channel()

    # exchange
    broker_channel.exchange_declare(exchange='BROKER', exchange_type='topic')
    bolsa_channel.exchange_declare(exchange='BOLSADEVALORES', exchange_type='topic')

    # queues
    broker_channel.queue_declare(queue='broker_q')

    '''binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)'''

    # consume
    broker_channel.queue_bind(exchange='BROKER', queue='broker_q', routing_key='#')

    print(' [*] Waiting for logs. To exit press CTRL+C')

    ordem_compra = []
    ordem_venda = []

    def read_message(routing_key, body):
        tipo, ativo = routing_key.split('.')
        body = str(body)
        quant, val, broker = body.split(',')
        quant = int(quant.split(':')[1])
        val = val.split(':')[1]
        broker = broker.split(':')[1][0:4]  # gets 4 first chars from string

        ordem = Ordem(tipo, ativo, quant, val, broker)
        if ordem.tipo == 'compra':
            ordem_compra.append(ordem)
        else:
            ordem_venda.append(ordem)

        return "ordem:", tipo, "ativo:", ativo, "qtd:", quant, "val:", val, "broker:", broker

    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
        # publish
        message = read_message(method.routing_key, body)
        bolsa_channel.basic_publish(exchange='BOLSADEVALORES', routing_key=method.routing_key, body=message)

    broker_channel.basic_consume(queue='broker_q', on_message_callback=callback, auto_ack=True)

    broker_channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
