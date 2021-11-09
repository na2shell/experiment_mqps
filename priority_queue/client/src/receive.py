import pika
import time
import sys
import glob
import os


def logger(pubtime,priority):
    os.remove("../log/log.txt")
    fw = open("../log/log.txt", "a")
    fw.write("%f [x] Received %f %r \n" % (time.time(), pubtime, priority))


if __name__ == "__main__":
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='broker', port=5672))
        channel = connection.channel()

        channel.queue_declare(queue='task2-rec')
        st_time = time.time()
        print(' [*] Waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            tmp = body.decode().split()
            pubtime = float(tmp[0])
            priority = tmp[1]
            print("%f [x] Received %f %r \n" %
                  (time.time(), pubtime, priority))
            logger(pubtime, priority)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=5)
        channel.basic_consume(queue='task2', on_message_callback=callback)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("==> catch interapt")
        sys.exit(0)
    except Exception as e:
        print(e)
