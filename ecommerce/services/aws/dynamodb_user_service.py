import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from django.conf import settings

from django.db.models import Model


class DynamoDbUserServiceController:
    def __init__(self) -> None:
        self.dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
            region_name="us-west-2",
            endpoint_url="http://dynamodb-local:8000",
        )
        self.products_table = self.dynamodb.Table("Products")

    def get_products_for_user(self, owner_id):
        try:
            response = self.products_table.query(
                IndexName="owner_id",
                KeyConditionExpression=Key("owner_id").eq(owner_id),
            )

            # Extract the items (products) from the response
            products = response.get("Items", [])

            return products
        except Exception as e:
            print(f"Error retrieving products for user: {str(e)}")
            return []

    def compare_products_for_sync(self, products: Model, user_id):
        try:
            # Query the DynamoDB table for products with the specified user_id
            response = self.products_table.query(
                IndexName="company_id",  # Replace with the actual index name if applicable
                KeyConditionExpression=Key("company_id").eq(user_id),
            )

            dynamodb_products = response.get("Items", [])

            local_products = products.objects.filter(
                owner_id=user_id, mark_for_sync=True
            )

            # Compare DynamoDB products with local products based on mark_for_sync
            products_to_sync = []
            for dynamodb_product in dynamodb_products:
                # Check if the DynamoDB product exists locally and is marked for sync
                matching_local_product = local_products.filter(
                    id=dynamodb_product["product_id"]
                ).first()
                if matching_local_product:
                    products_to_sync.append(matching_local_product)

            return products_to_sync
        except Exception as e:
            print(f"Error comparing products for sync: {str(e)}")
            return []

    def upload_or_update_product(self, product):
        """
        Upload or update a product in DynamoDB.

        Args:
            product (Product): The product object to upload or update.

        Returns:
            dict: The response from DynamoDB.
        """
        try:
            table = self.dynamodb.Table("Products")  # Replace with your table name
            response = None

            # Check if the product already exists in DynamoDB by checking its primary key
            existing_product = table.query(
                IndexName="Products",  # Replace with your index name
                KeyConditionExpression=Key("product_id").eq(product.id),
            )

            if existing_product["Count"] > 0:
                # If the product exists, update it
                response = table.update_item(
                    Key={"product_id": product.id},
                    UpdateExpression="SET #name = :name, #description = :description, #price = :price, #available = :available, #stock = :stock, #listed = :listed, #mark_for_sync = :mark_for_sync",
                    ExpressionAttributeNames={
                        "#name": "name",
                        "#description": "description",
                        "#price": "price",
                        "#available": "available",
                        "#stock": "stock",
                        "#listed": "listed",
                        "#mark_for_sync": "mark_for_sync",
                    },
                    ExpressionAttributeValues={
                        ":name": product.name,
                        ":description": product.description,
                        ":price": product.price,
                        ":available": product.available,
                        ":stock": product.stock,
                        ":mark_for_sync": product.mark_for_sync,
                    },
                    ReturnValues="ALL_NEW",
                )
            else:
                # If the product does not exist, create it
                response = table.put_item(
                    Item={
                        "product_id": product.id,  # Replace with your primary key field
                        "name": product.name,
                        "description": product.description,
                        "price": product.price,
                        "available": product.available,
                        "stock": product.stock,
                        "mark_for_sync": product.mark_for_sync,
                    }
                )

            return response

        except Exception as e:
            # Handle any exceptions here
            print(f"Error uploading/updating product to DynamoDB: {e}")
            return None
