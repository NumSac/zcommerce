from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    UnicodeSetAttribute,
    BooleanAttribute,
)
from pynamodb.exceptions import DoesNotExist
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from typing import List
from marshmallow import Schema, fields
from services.aws.dynamodb_repository import DynamoDBRepository
from .base_model import DynamoDbBaseModel


# DynamoDb Global Secondary index for querying registration_number
class RegistrationNumberIndex(GlobalSecondaryIndex):
    class Meta:
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    registration_number = UnicodeAttribute(hash_key=True)


# Implement Category Global Secondary Index


# Pynamodb ORM model
class Product(DynamoDbBaseModel):
    class Meta(DynamoDbBaseModel.Meta):
        table_name = "Products"

    product_id = UnicodeAttribute(hash_key=True)
    # product_image = UnicodeAttribute()
    title = UnicodeAttribute()
    description = UnicodeAttribute()
    categories = UnicodeSetAttribute()
    available = BooleanAttribute()
    slug = UnicodeAttribute()
    stock = NumberAttribute()
    price = UnicodeAttribute()
    registration_number_index = RegistrationNumberIndex()
    registration_number = UnicodeAttribute()


# Serializer model from marshmallow
class ProductSerializer(Schema):
    class Meta:
        model = Product
        projection = AllProjection

    product_id = fields.Str()
    # product_image = fields.Str()
    title = fields.Str()
    description = fields.Str()
    categories = fields.List(fields.String())
    available = fields.Bool()
    stock = fields.Int()
    slug = fields.Str()
    price = fields.Decimal(as_string=True)
    registration_number = fields.Str()


# Dynamodb Repository for Products
class ProductRepository(DynamoDBRepository):
    def __init__(self):
        super().__init__(Product)

    def get_products_by_registration_number(self, registration_number: str) -> List:
        try:
            products = Product.registration_number_index.query(registration_number)

            product_list = list(products)

            return product_list
        except DoesNotExist:
            return []
        except Exception as e:
            print(f"Error retrieving products: {str(e)}")
            return []
