import boto3
from botocore.exceptions import ClientError
from django.conf import settings


class DynamoDbTable:
    def __init__(self, table_name, key_schema, attribute_definitions, throughput):
        self.dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION_NAME)
        self.table_name = table_name
        self.key_schema = key_schema
        self.attribute_definitions = attribute_definitions
        self.throughput = throughput

    def create_table(self):
        try:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=self.key_schema,
                AttributeDefinitions=self.attribute_definitions,
                ProvisionedThroughput=self.throughput,
            )
            table.meta.client.get_waiter("table_exists").wait(TableName=self.table_name)
            print(
                f"{self.table_name} Table has been created. Table status:",
                table.table_status,
            )
        except ClientError as err:
            print(f"Failed to create table {self.table_name}: {err}")
            return False
        return True


class UsersTable(DynamoDbTable):
    def __init__(self):
        super().__init__(
            table_name="Users",
            key_schema=[
                {"AttributeName": "username", "KeyType": "HASH"}  # Partition key
            ],
            attribute_definitions=[
                {"AttributeName": "username", "AttributeType": "S"},
            ],
            throughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )


class CompanyTable(DynamoDbTable):
    def __init__(self):
        super().__init__(
            table_name="Company",
            key_schema=[
                {
                    "AttributeName": "registration_number",
                    "KeyType": "HASH",
                }  # Partition key
            ],
            attribute_definitions=[
                {"AttributeName": "registration_number", "AttributeType": "S"},
            ],
            throughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )


class ProductsTable(DynamoDbTable):
    def __init__(self):
        super().__init__(
            table_name="Products",
            key_schema=[
                {"AttributeName": "product_id", "KeyType": "HASH"}  # Partition key
            ],
            attribute_definitions=[
                {"AttributeName": "product_id", "AttributeType": "S"},
                {"AttributeName": "category", "AttributeType": "S"},
            ],
            throughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        # Additional attributes for this table, such as GlobalSecondaryIndexes, can be added here.


class ShoppingCartTable(DynamoDbTable):
    def __init__(self):
        super().__init__(
            table_name="ShoppingCart",
            key_schema=[
                {"AttributeName": "username", "KeyType": "HASH"}  # Partition key
            ],
            attribute_definitions=[
                {"AttributeName": "username", "AttributeType": "S"},
                # Assuming items are stored as a String Set or List. DynamoDB handles this internally.
            ],
            throughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )


# Usage
users_table = UsersTable()
users_table.create_table()

company_table = CompanyTable()
company_table.create_table()

products_table = ProductsTable()
products_table.create_table()
