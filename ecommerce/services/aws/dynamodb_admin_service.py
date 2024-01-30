from pynamodb.connection.base import Connection
from pynamodb.exceptions import TableDoesNotExist
from pynamodb.models import Model
from pynamodb.exceptions import TableDoesNotExist


class DynamoDbAdminServiceController:
    def __init__(self):
        self.connection = Connection(
            aws_access_key_id="dummy",
            region="dummy",
            aws_secret_access_key="dummy",
            host="http://dynamodb-local:8000",
        )

    def get_db_metadata(self):
        try:
            tables = self.connection.list_tables()

            # Fetching the list of all tables
            table_list = [table for table in tables]

            # Getting details and item count of each table
            table_details = []
            for table_name in table_list:
                try:
                    table_info = self.connection.describe_table(table_name)
                    table_details.append(
                        {
                            "TableName": table_name,
                            "ItemCount": table_info.item_count,
                        }
                    )
                except TableDoesNotExist:
                    continue

            return {
                "DBOnline": True,
                "TableList": table_list,
                "TableDetails": table_details,
            }

        except Exception as e:
            print(f"Error retrieving DynamoDB metadata: {str(e)}")
            return {"DBOnline": False}

    def delete_table(self, table_name: str) -> bool:
        try:
            tables = self.connection.list_tables()
            if not table_name in tables.values():
                raise TableDoesNotExist(
                    f"Error when deleting table. {table_name} does not exist"
                )
            self.connection.delete_table(table_name)
            return True

        except Exception as err:
            print(err)
            raise err

    def delete_item(self, table_name: str, item_id) -> object:
        return object()
