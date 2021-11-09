# *- utf-8 -*
import pika
import time
import sys
import ssl

if __name__ == "__main__":
    try:

        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_verify_locations("./cert/ca_certificate.pem")

        context = ssl.create_default_context(
        cafile="./cert/ca_certificate.pem")
        context.load_cert_chain("./cert/client_certificate.pem",
                        "./cert/client_key.pem")

        cp = pika.ConnectionParameters(port=5671,
            ssl_options=pika.SSLOptions(context, "localhost"))

        # parameters = pika.URLParameters("amqp://localhost:8885")
        """
        parameters_tls = pika.URLParameters("amqps://localhost:5671")
        parameters_tls_dck = pika.URLParameters(
            "amqps://guest:guest@broker:5671")
        """

        conn = pika.BlockingConnection(cp)
        channel = conn.channel()

        channel.queue_declare(queue='task-rec')
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
