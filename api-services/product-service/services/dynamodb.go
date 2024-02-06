package services

import (
	"context"
	"log"

	types "github.com/NumSac/product-service/data"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/expression"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

type TableConfig struct {
	DynamoDbClient *dynamodb.Client
	TableName      string
}

func (tblConfig TableConfig) Query(registrationNumber string) {
	var err error
	var response *dynamodb.QueryOutput
	var products []types.Product

	keyEx := expression.Key("registration_number").Equal(expression.Value(registrationNumber))
	expr, err := expression.NewBuilder().WithKeyCondition(keyEx).Build()
	if err != nil {
		log.Printf("[!] Couldn't build expression for query: %v\n", err)
	} else {
		queryPaginator := dynamodb.NewQueryPaginator(tblConfig.DynamoDbClient, &dynamodb.QueryInput{
			TableName:                 aws.String(tblConfig.TableName),
			ExpressionAttributeNames:  expr.Names(),
			ExpressionAttributeValues: expr.Values(),
			KeyConditionExpression:    expr.KeyCondition(),
		})
		for queryPaginator.HasMorePages() {
			response, err = queryPaginator.NextPage(context.TODO())
			if err != nil {
				log.Printf("[!] Couldn't query company for registration_id released in %v\n: ", registrationNumber)
				break
			} else {
				var productPage []types.Product
				err = attributevalue.UnmarshalListOfMaps(response.Items, &productPage)
				if err != nil {
					log.Printf("Couldn't unmarshal query response. Here's why: %v\n", err)
					break

				} else {
					products = append(products, productPage...)
				}

			}
		}
	}
}
