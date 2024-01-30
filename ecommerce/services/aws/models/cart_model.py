from services.aws.dynamodb_repository import DynamoDBRepository
from .base_model import DynamoDbBaseModel


class Cart(DynamoDbBaseModel):
    class Meta(DynamoDbBaseModel.Meta):
        table_name = "Cart"
