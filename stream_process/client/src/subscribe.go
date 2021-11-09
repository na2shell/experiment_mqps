package main

import (
	"bufio"
	"fmt"
	"os"
	"time"

	"github.com/google/uuid"
	"github.com/rabbitmq/rabbitmq-stream-go-client/pkg/amqp"
	"github.com/rabbitmq/rabbitmq-stream-go-client/pkg/stream"
)

func sub() {
	reader := bufio.NewReader(os.Stdin)
	env, err := stream.NewEnvironment(
		stream.NewEnvironmentOptions().
			SetHost("broker").
			SetPort(5552).
			SetUser("guest").
			SetPassword("guest"))
	CheckErr(err)

	streamName := uuid.New().String()
	err = env.DeclareStream(streamName,
		&stream.StreamOptions{
			MaxLengthBytes: stream.ByteCapacity{}.GB(2),
		},
	)

	CheckErr(err)

	// Define a consumer per stream, there are different offset options to define a consumer, default is
	//env.NewConsumer(streamName, func(Context streaming.ConsumerContext, message *amqp.Message) {
	//
	//}, nil)
	// if you need to track the offset you need a consumer name like:
	handleMessages := func(consumerContext stream.ConsumerContext, message *amqp.Message) {
		fmt.Printf("consumer name: %s, text: %s \n ", consumerContext.Consumer.GetName(), message.Data)
	}

	consumer, err := env.NewConsumer(
		streamName,
		handleMessages,
		stream.NewConsumerOptions().
			SetConsumerName("my_consumer").                  // set a consumer name
			SetOffset(stream.OffsetSpecification{}.First())) // start consuming from the beginning
	CheckErr(err)
	channelClose := consumer.NotifyClose()
	// channelClose receives all the closing events, here you can handle the
	// client reconnection or just log
	defer consumerClose(channelClose)

	fmt.Println("Press any key to stop ")
	_, _ = reader.ReadString('\n')
	err = consumer.Close()
	time.Sleep(200 * time.Millisecond)
	CheckErr(err)
	err = env.DeleteStream(streamName)
	CheckErr(err)
	err = env.Close()
	CheckErr(err)
}
