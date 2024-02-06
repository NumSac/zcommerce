package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"sync"

	"github.com/aws/aws-sdk-go-v2/aws"
	awsConfigMod "github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

var awsConfig aws.Config
var onceAwsConfig sync.Once

var dynamodbClient *dynamodb.Client
var onceDbClient sync.Once

const webPort = "80"

type Config struct{}

func main() {

	app := Config{}

	srv := &http.Server{
		Addr:    fmt.Sprintf(":%s", webPort),
		Handler: app.routes(),
	}

	log.Printf("[*] Starting product service on port %s\n", webPort)
	err := srv.ListenAndServe()
	if err != nil {
		log.Panic(err)
	}
}

func getAwsConfig() aws.Config {
	onceAwsConfig.Do(func() {
		var err error
		awsConfig, err = awsConfigMod.LoadDefaultConfig(context.TODO())
		if err != nil {
			log.Panic(err)
		}
	})

	return awsConfig
}

func GetDynamoDbClient() *dynamodb.Client {
	onceDbClient.Do(func() {
		awsConfig = getAwsConfig()

		region := awsConfig.Region
		// Add the rest of the aws config

		dynamodbClient = dynamodb.NewFromConfig(awsConfig, func(opt *dynamodb.Options) {
			opt.Region = region
		})
	})

	return dynamodbClient
}
