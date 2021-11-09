import pika
import sys
import time



def p_message(n):
    mes = str(time.time()) + " message"
    channel.basic_publish(
        exchange='',
        routing_key='task2',
        body=mes,
        properties=pika.BasicProperties(
            delivery_mode=1,  # make message persistent
        ))
    print(" [%d] Sent %r" % (n,mes))

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

channel.queue_declare(queue='task-ms')
mes = "hello"
channel.basic_publish(
    exchange='',
    routing_key='task-ms',
    body=mes,
    properties=pika.BasicProperties(
        delivery_mode=1,  # make message persistent
    ))
#p_message(1)
connection.close()
   
    