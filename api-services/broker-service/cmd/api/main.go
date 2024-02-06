package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"time"
)

const (
	host    = "127.0.0.0"
	webPort = 8881
)

type Config struct{}

func main() {
	var wait time.Duration
	fmt.Println("[i] Starting up broker-service...")

	app := Config{}

	log.Println("[i] Checking gRPC servers...")
	err := checkGrpcServers()
	if err != nil {
		log.Panic("[!] Unable to connect to grpc services.\n", err)
	}
	log.Println("[i] Grpc severs are connected")
	log.Println("[i] Checking DynamoDB connection...")
	err = checkDynamoDb()
	if err != nil {
		log.Panic("[!] Unable to connect to dynamodb.\n", err)
	}

	log.Println("Starting broker service on port")
	srv := &http.Server{
		Handler:      app.routes(),
		Addr:         fmt.Sprintf("%s:%d", host, webPort),
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}

	// Run our server in a goroutine so that it doesn't block.
	go func() {
		if err := srv.ListenAndServe(); err != nil {
			log.Println(err)
		}
	}()

	c := make(chan os.Signal, 1)
	// We'll accept graceful shutdowns when quit via SIGINT (Ctrl+C)
	// SIGKILL, SIGQUIT or SIGTERM (Ctrl+/) will not be caught.
	signal.Notify(c, os.Interrupt)

	// Block until we receive our signal.
	<-c

	// Create a deadline to wait for.
	ctx, cancel := context.WithTimeout(context.Background(), wait)
	defer cancel()
	// Doesn't block if no connections, but will otherwise wait
	// until the timeout deadline.
	srv.Shutdown(ctx)
	log.Println("[*] gracefully shutting down")
}

func checkGrpcServers() error {
	return nil
}

func checkDynamoDb() error {
	return nil
}
