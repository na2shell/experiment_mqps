import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='l-rabit'))
channel = connection.channel()

channel.queue_declare(queue='task', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
for i in range(3000):
    message_num = str(i)
    channel.basic_publish(
        exchange='',
        routing_key='task',
        body=message_num,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent %r" % message_num)

connection.close()