from marshmallow import Schema, fields


from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute

from services.aws.dynamodb_repository import DynamoDBRepository
from .base_model import DynamoDbBaseModel


class Company(DynamoDbBaseModel):
    class Meta(DynamoDbBaseModel.Meta):
        table_name = "Companies"

    company_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute()
    # background_image_url = UnicodeAttribute()
    registration_number = UnicodeAttribute()
    vat_number = UnicodeAttribute()


class CompanySerializer(Schema):
    company_id = fields.Int()
    name = fields.String()
    # background_image_url = fields.String()
    registration_number = fields.String()
    vat_number = fields.String()


class CompanyRepository(DynamoDBRepository):
    def __init__(self):
        super().__init__(Company)
