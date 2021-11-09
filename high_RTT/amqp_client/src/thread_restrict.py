import functools
import logging
import pika
import threading
import logging.handlers
import time
import random
import concurrent.futures


def ack_message(channel, delivery_tag):
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        pass


def do_work(connection, channel, delivery_tag, body):
    thread_id = threading.get_ident()
    fmt1 = 'Thread id: {} Delivery tag: {} Message body: {}'
    LOGGER.info(fmt1.format(thread_id, delivery_tag, body))
    sleep_seconds = 0.05
    time.sleep(sleep_seconds)

    fmt2 = 'body: {} time: {}'
    LOGGER.info(fmt2.format(body, time.time()))

    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)


def on_message_callback(channel, method_frame, header_frame, body, args):
    (executor, func) = args
    delivery_tag = method_frame.delivery_tag
    target = do_work(connection, channel, delivery_tag, body)
    executor.submit(target)


if __name__ == "__main__":
	LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
					'-35s %(lineno) -5d: %(message)s')
	LOGGER = logging.getLogger(__name__)
	LOGGER.addHandler(logging.handlers.RotatingFileHandler(
	filename='./sample.log', maxBytes=10000000, backupCount=15))

	logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
	connection = pika.BlockingConnection(
	pika.ConnectionParameters(host='l-rabit'))
	channel = connection.channel()
	channel.queue_declare(queue='task', durable=True)
	channel.basic_qos(prefetch_count=60)

	executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
	channel.basic_consume(
		queue='task', on_message_callback=on_message_callback("hoge"))
	try:
		channel.start_consuming()
	except KeyboardInterrupt:
		channel.stop_consuming()

#まだ動かしていない。書いている途中