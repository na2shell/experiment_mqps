import paho
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from multiprocessing import Pool
import random


def get_and_save(client_id):
    topics = "#"
    mes = subscribe.simple(topics, qos=0, msg_count=1, retained=False, hostname="broker",
                           port=1883, client_id=client_id, keepalive=60, will=None, auth=None, tls=None,
                           protocol=mqtt.MQTTv311)

    filename = "sample_" + str(random.randint(100, 900)) + ".dat"

    f = open(filename, "wb")
    f.write(mes.payload)
    print("end")


if __name__ == "__main__":
    arg_list = ["client-1","client-2"]
    with Pool(processes=2) as p:
        p.map(func=get_and_save, iterable=arg_list)
