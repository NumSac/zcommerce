from typing import List, Optional
from pynamodb.models import Model
from .models.product_model import Product as ProductModel


class DynamoDbUserServiceController:
    def __init__(self) -> None:
        self.product_model = ProductModel

    def get_products_for_user(self, registration_number: str) -> List[ProductModel]:
        try:
            # Query the DynamoDB table for products with the specified owner_id
            products = self.product_model.query(str(registration_number))
            return list(products)
        except Exception as e:
            print(f"Error retrieving products for user: {str(e)}")
            return []

    def compare_products_for_sync(self, products, registration_number: str) -> List:
        try:
            # Query the DynamoDB table for products with the specified registration_number
            dynamodb_products = self.product_model.query(str(registration_number))
            # Create a dictionary of DynamoDB products for efficient lookup
            dynamodb_product_dict = {
                str(p.company_registration_number): p for p in dynamodb_products
            }
            # Compare DynamoDB products with provided products based on mark_for_sync
            products_to_sync = [
                product
                for product in products
                if (str(product.registration_number) in dynamodb_product_dict)
            ]
            return products_to_sync
        except Exception as e:
            print(f"Error comparing products for sync: {str(e)}")
            return []

    def upload_or_update_product(
        self, product, registration_number: str
    ) -> Optional[ProductModel]:
        try:
            # Try to get the existing product from DynamoDB
            existing_product = self.product_model.get(product.id)

            # Update the attributes of the existing product
            existing_product.title = product.title
            # existing_product.product_image = product.product_image
            existing_product.category = product.category.name
            existing_product.price = str(product.price)
            existing_product.description = product.description
            existing_product.registration_number = registration_number

            # Save the updated product
            existing_product.save()

            return existing_product

        except self.product_model.DoesNotExist:
            # If the product does not exist, create a new one
            new_product = self.product_model(
                **{
                    "product_id": product.id,
                    # "product_image": product.product_image,
                    "title": product.title,
                    "category": product.category,
                    "price": str(product.price),
                    "description": product.description,
                    "registration_number": registration_number,
                }
            )
            new_product.save()
            return new_product

        except Exception as e:
            print(f"Error uploading/updating product to DynamoDB: {e}")
            return None
