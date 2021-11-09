import functools
import logging
import pika
import threading
import logging.handlers
import time
import random
import concurrent.futures

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.handlers.RotatingFileHandler(
    filename='./sample.log', maxBytes=10000000, backupCount=15))

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def ack_message(channel, delivery_tag):
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        pass

def do_work(connection, channel, delivery_tag, body):
    thread_id = threading.get_ident()
    fmt1 = 'Thread id: {} Delivery tag: {} Message body: {}'
    LOGGER.info(fmt1.format(thread_id, delivery_tag, body))
    # Sleeping to simulate 10 seconds of work
    #sleep_seconds = random.randint(2, 4)
    sleep_seconds = 0.05
    time.sleep(sleep_seconds)
    fmt2 = 'body: {} time: {}'
    LOGGER.info(fmt2.format(body,time.time()))
    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)

def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(connection, channel, delivery_tag, body))
    t.start()
    threads.append(t)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='l-rabit'))
channel = connection.channel()
channel.queue_declare(queue='task', durable=True)
channel.basic_qos(prefetch_count=60)

threads = []
on_message_callback = functools.partial(on_message, args=(connection, threads))
channel.basic_consume(queue='task',on_message_callback=on_message_callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# Wait for all to complete
for thread in threads:
    thread.join()

connection.close()
