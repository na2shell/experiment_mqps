package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"io/ioutil"
	"log"

	"github.com/streadway/amqp"
)

var amqpURI string = "amqps://localhost:8881"

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
		panic(fmt.Sprintf("%s: %s", msg, err))
	}
}

func main() {
	cfg := new(tls.Config)

	// see at the top
	cfg.RootCAs = x509.NewCertPool()

	if ca, err := ioutil.ReadFile("./cacert.pem"); err == nil {
		cfg.RootCAs.AppendCertsFromPEM(ca)
	}

	conn, err := amqp.DialTLS(amqpURI, cfg)
	failOnError(err, "Failed to connect to MQ")
	defer conn.Close()

	channel, err := conn.Channel()
	failOnError(err, "Failed to open a channel")

	q, err := channel.QueueDeclare(
		"my-queue", // name
		false,      // durable
		false,      // delete when unused
		false,      // exclusive
		false,      // no-wait
		nil,        // arguments
	)
	failOnError(err, "Failed to declare a queue")

	messages, err := channel.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // arguments
	)
	failOnError(err, "Failed to register a consumer")

	forever := make(chan bool)

	go func() {
		for data := range messages {
			log.Printf("%s\n", data.Body)
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C\n")
	<-forever
}
