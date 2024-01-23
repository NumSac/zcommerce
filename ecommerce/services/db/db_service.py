from ecommerce.products.models import Product, Category
from ecommerce.util.serializers import serialize_product_to_dynamodb_dto
import subprocess, os, stat
import boto3

from django.conf import settings
from django.db.models import Model
from django.core.serializers import serialize

from typing import List


def get_dynamodb_resource():
    return boto3.resource("dynamodb", region_name="region-name")


# DbService for User/Company manual sync requests
class DbService:
    def __init__(self) -> None:
        try:
            self.dynamodb = get_dynamodb_resource()
        except Exception as err:
            print("[!] Could not get dynamodb instance")
            raise err

    @staticmethod
    def sync_company_products_with_dynamodb(
        self, products: Product, company_id: str
    ) -> bool:
        try:
            company_products_snapshot = products.objects.all(owner=company_id)
            # Select the DynamoDb table
            table = self.dynamodb.Table("shop_products")
            for product in company_products_snapshot:
                serialized_product = serialize_product_to_dynamodb_dto(product)
                table.put_item(serialized_product)

        except Exception as err:
            raise err

        return True

    def update_product(self, update_data, product_id):
        try:
            table = self.dynamodb.Table("Products")

            # Define the update expression and attribute values
            update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in update_data)
            attribute_values = {f":{k}": v for k, v in update_data.items()}

            response = table.update_item(
                Key={"product_id": product_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=attribute_values,
            )
            return response
        except Exception as err:
            print("Could not updat product")

    @staticmethod
    def backup_company_products(self, company_id: str):
        pass


# Admin global Db Control
class AdminDbService:
    @staticmethod
    def sync_products_with_dynamodb():
        # Get the DynamoDB resource
        dynamodb = get_dynamodb_resource()

        # Select the DynamoDb table
        table = dynamodb.Table("shop_products")

    @staticmethod
    def snapshot_table_for_dynamodb(table: Model) -> List:
        try:
            entities = table.objects.all()

            serialized_entities = serialize("json", entities)
        except Exception as err:
            raise err

    @staticmethod
    def backup_database(self, destination: str):
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        # Call the dumpdatabase command
        with open(destination, "w") as file:
            subprocess.run(
                ["python", "manage.py", "dumpdata"],
                stdout=file,  # Output the data to the backup file
                stderr=subprocess.PIPE,  # Capture any error messages
                text=True,
            )
        self.adjust_backup_file_permissions(destination)

        return True

    @staticmethod
    def backup_table(self, destination: str, db_object: Model) -> bool:
        try:
            # Serialize to Jspon
            data = serialize("json", db_object.objects.all())

            # Ensure the destination directorey exists
            os.makedirs(os.path.dirname(destination), exist_ok=True)

            # Write the data to the destination file
            with open(destination, "w") as file:
                file.write(data)

            self.adjust_backup_file_permissions(destination)

            print(f"Backup of {db_object.__name__} completed successfully.")
            return True

        except Exception as err:
            print(f"An error occurred while backing up {db_object.__name__}: {err}")
            return False

    @staticmethod
    def adjust_backup_file_permissions(self, destination_file: str) -> bool:
        try:
            # Ensure bak file
            if not destination_file.endswith(".bak"):
                print("[!] File is not a backup file")
                return False
            os.chmod(destination_file, stat.S_IRUSR | stat.S_IWUSR)
        except Exception as err:
            print(
                f"An error occured while trying to adjust permission of {destination_file.__name__}: {err}"
            )
            return False
