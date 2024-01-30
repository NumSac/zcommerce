from pynamodb.attributes import (
    UnicodeAttribute,
)


from marshmallow import Schema, fields

from services.aws.dynamodb_repository import DynamoDBRepository
from .base_model import DynamoDbBaseModel


class User(DynamoDbBaseModel):
    class Meta(DynamoDbBaseModel.Meta):
        table_name = "Users"

    user_id = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute()
    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    email = UnicodeAttribute()


class UserSerializer(Schema):
    user_id = fields.String()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()


class UserRepository(DynamoDBRepository):
    def __init__(self):
        super().__init__(User)
