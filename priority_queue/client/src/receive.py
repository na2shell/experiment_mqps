import pika
import time
import sys
import glob
import os
import requests


def logger(pubtime, priority, kind, file_name):
    fw = open("../log/log.txt", "a")
    fw.write(
        "%f [%s] Received %s %f %r \n"
        % (time.time(), file_name, kind, pubtime, priority)
    )


def http_request(file_name, logger, pubtime, priority):
    url = "http://web/" + file_name
    file_path = "/home/download/" + file_name
    res = requests.get(url, stream=True)
    if res.status_code != 200:
        raise ValueError("error!")

    with open(file_path, "wb") as file:
        for chunk in res.iter_content(chunk_size=1024):
            file.write(chunk)

    print("suc: ", file_name)
    logger(pubtime, priority, "HTTP", file_name)


if __name__ == "__main__":
    try:
        os.remove("../log/log.txt")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="broker", port=5672)
        )
        channel = connection.channel()
        st_time = time.time()
        print(" [*] Waiting for messages. To exit press CTRL+C")

        def callback(ch, method, properties, body):
            tmp = body.decode().split(",")
            pubtime = float(tmp[0])
            priority = int(tmp[1])
            file_name = tmp[2]
            print("%f [x] Received %f %r \n" % (time.time(), pubtime, priority))
            logger(pubtime, priority, "MQPs", file_name)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            http_request(file_name, logger, pubtime, priority)

        channel.basic_qos(prefetch_count=5)
        channel.basic_consume(queue="task2", on_message_callback=callback)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("==> catch interapt")
        sys.exit(0)
    except Exception as e:
        print(e)
