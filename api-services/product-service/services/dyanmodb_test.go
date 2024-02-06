package services

import (
	"errors"
	"testing"

	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/sso/types"
	"github.com/awsdocs/aws-doc-sdk-examples/gov2/testtools"
)

func enterTest() (*testtools.AwsmStubber, *TableConfig) {
	stubber := testtools.NewStubber()
	basics := &TableConfig{TableName: "test-table", DynamoDbClient: dynamodb.NewFromConfig(*stubber.SdkConfig)}
	return stubber, basics
}

func TableExists(raiseErr *testtools.StubError, t *testing.T) {
	stubber, basics := enterTest()
	stubber.Add(stubs.StubDescribeTable(basics.TableName, raiseErr))

	exists, err := basics.TableExists()

	testtools.VerifyError(err, raiseErr, t, &types.ResourceNotFoundException{})
	var nfEx *types.ResourceNotFoundException
	if raiseErr == nil && !exists {
		t.Errorf("Expected to exist.\n")
	} else if errors.As(raiseErr, &nfEx) && exists {
		t.Errorf("Expected not exists, got %v.", exists)
	}

	testtools.ExitTest(stubber, t)
}
