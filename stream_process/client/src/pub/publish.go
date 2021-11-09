package main

import (
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/google/uuid"
	"github.com/rabbitmq/rabbitmq-stream-go-client/pkg/amqp"
	"github.com/rabbitmq/rabbitmq-stream-go-client/pkg/logs"
	"github.com/rabbitmq/rabbitmq-stream-go-client/pkg/stream"
)

func CheckErr(err error) {
	if err != nil {
		fmt.Printf("%s ", err)
		os.Exit(1)
	}
}

func handlePublishConfirm(confirms stream.ChannelPublishConfirm) {
	go func() {
		for confirmed := range confirms {
			for _, msg := range confirmed {
				if msg.Confirmed {
					fmt.Printf("message %s stored \n  ", msg.Message.GetData())
				} else {
					fmt.Printf("message %s failed \n  ", msg.Message.GetData())
				}

			}
		}
	}()
}

func main() {
	// Set log level, not mandatory by default is INFO
	stream.SetLevelInfo(logs.DEBUG)

	fmt.Println("Getting started with Streaming client for RabbitMQ")
	fmt.Println("Connecting to RabbitMQ streaming ...")

	// Connect to the broker ( or brokers )
	env, err := stream.NewEnvironment(
		stream.NewEnvironmentOptions().
			SetHost("broker").
			SetPort(5552).
			SetUser("guest").
			SetPassword("guest"))
	CheckErr(err)
	// Create a stream, you can create streams without any option like:
	// err = env.DeclareStream(streamName, nil)
	// it is a best practise to define a size,  1GB for example:

	streamName := uuid.New().String()
	fmt.Print(streamName)
	err = env.DeclareStream(streamName,
		&stream.StreamOptions{
			MaxLengthBytes: stream.ByteCapacity{}.GB(2),
		},
	)

	CheckErr(err)

	// Get a new producer for a stream
	producer, err := env.NewProducer(streamName, nil)
	CheckErr(err)

	//optional publish confirmation channel
	chPublishConfirm := producer.NotifyPublishConfirmation()
	handlePublishConfirm(chPublishConfirm)

	// the send method automatically aggregates the messages
	// based on batch size
	for i := 0; i < 10; i++ {
		err := producer.Send(amqp.NewMessage([]byte("hello_world_" + strconv.Itoa(i))))
		CheckErr(err)
	}

	time.Sleep(1 * time.Second)
	err = producer.Close()
	CheckErr(err)
	fmt.Printf("produce end")
}
