import pika
import sys
import time
import random
import uuid
import subprocess

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="broker", port=5672)
)
channel = connection.channel()

args = {"x-max-priority": 5}
channel.queue_declare(queue="task2", arguments=args)


def logger(mes):
    fw = open("../log/log_send.txt", "a")
    fw.write("%s\n" % (mes))


def p_message(n, mes, _priority):
    channel.basic_publish(
        exchange="",
        routing_key="task2",
        body=mes,
        properties=pika.BasicProperties(
            priority=_priority,
            delivery_mode=1,  # make message persistent
        ),
    )
    print(" [%d] Sent %r" % (n, mes))
    logger(mes)


def make_file(vol):
    filename = str(uuid.uuid4()) + ".dat"
    path = "/home/data/" + filename
    subprocess.run(["fallocate", "-l", vol, path])
    return filename


if __name__ == "__main__":
    for i in range(100):
        p = random.randint(1, 5)

        if p > 3:
            filename = make_file("10k")
        else:
            filename = make_file("500b")

        mes = ",".join([str(time.time()), str(p), filename])
        p_message(i, mes, p)
        # time.sleep(0.1)

    connection.close()
