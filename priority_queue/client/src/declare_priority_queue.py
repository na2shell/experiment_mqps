import pika
import sys
import time
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='broker', port=5672))
channel = connection.channel()

args = {"x-max-priority": 5}
channel.queue_declare(queue='task2', arguments=args)

def p_message(n,_priority):
    mes = str(time.time()) + " message-pr" + str(_priority)
    channel.basic_publish(
        exchange='',
        routing_key='task2',
        body=mes,
        properties=pika.BasicProperties(
            priority=_priority,
            delivery_mode=1,  # make message persistent
        ))
    print(" [%d] Sent %r" % (n,mes))

for i in range(1000):
    random.seed()
    p = random.randint(1,5)
    p_message(i,p)
    time.sleep(0.1)


connection.close()