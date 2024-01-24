import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from django.conf import settings

from django.db.models import Model


class DynamoDbAdminServiceController:
    def __init__(self) -> None:
        self.dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
            region_name="us-west-2",
            endpoint_url="http://dynamodb-local:8000",
        )
        self.client = boto3.client(
            "dynamodb",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
            region_name="us-west-2",
            endpoint_url="http://dynamodb-local:8000",
        )

    def get_db_metadata(self):
        try:
            # Check if DynamoDB is online
            self.client.list_tables(Limit=1)
            db_online = True

            # Fetching the list of all tables
            table_list = self.client.list_tables()

            # Getting details and item count of each table
            table_details = []
            for table_name in table_list["TableNames"]:
                table_info = self.client.describe_table(TableName=table_name)
                table_info["Table"]["ItemCount"] = self.client.describe_table(
                    TableName=table_name
                )["Table"]["ItemCount"]
                table_details.append(table_info["Table"])

        except ClientError as e:
            print(e.response["Error"]["Message"])
            db_online = False
            return {"DBOnline": db_online}
        else:
            return {
                "DBOnline": db_online,
                "TableList": table_list["TableNames"],
                "TableDetails": table_details,
            }

    def sync_all_dynamodb_tables(self):
        return

    def sync_dynamodb_table(self):
        return
