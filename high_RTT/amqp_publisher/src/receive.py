import pika
import time
from concurrent import futures

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='l-rabit'))
channel = connection.channel()

channel.queue_declare(queue='task', durable=True)
st_time = time.time()
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    if(body.decode() == "2999"):
        print(time.time()-st_time)

    time.sleep(0.05)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=6)
channel.basic_consume(queue='task', on_message_callback=callback)

channel.start_consuming()