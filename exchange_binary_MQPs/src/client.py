import paho
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

if __name__ == "__main__":
    topic = "/binary/image"
    f = open("image.jpeg","rb")
    image = f.read()
    print(type(image))
    bitarr = bytearray(image)
    print(type(bitarr))

    _payload = image

    publish.single(topic, payload=_payload, qos=0, retain=False, hostname="broker",
        port=1883, client_id="r-cliinet-1", keepalive=60, will=None, auth=None, tls=None,
        protocol=mqtt.MQTTv311, transport="tcp")
