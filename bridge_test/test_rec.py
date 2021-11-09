import pika
import time
import sys

if __name__ == "__main__":
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', port=5673))
        channel = connection.channel()

        channel.queue_declare(queue='task2-rec')
        st_time = time.time()
        print(' [*] Waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print("%f [x] Received %r \n" %
                  (time.time(), body.decode()))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='task-ms', on_message_callback=callback)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("==> catch interapt")
        sys.exit(0)
    except Exception as e:
        print(e)