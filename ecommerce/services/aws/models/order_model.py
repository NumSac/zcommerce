from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    MapAttribute,
)
from .base_model import DynamoDbBaseModel
from services.aws.dynamodb_repository import DynamoDBRepository


class OrderDetails(MapAttribute):
    pass


class Order(DynamoDbBaseModel):
    class Meta(DynamoDbBaseModel.Meta):
        table_name = "Orders"

    order_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute()
    order_details = OrderDetails()


class OrderRepository(DynamoDBRepository):
    def __init__(self):
        super().__init__(Order)
