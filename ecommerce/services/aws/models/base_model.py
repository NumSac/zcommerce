from pynamodb.models import Model


class DynamoDbBaseModel(Model):
    class Meta:
        abstract = True
        host = "http://dynamodb-local:8000"
        aws_access_key_id = "dummy"
        region = "dummy"
        aws_secret_access_key = "dummy"
        read_capacity_units = 10
        write_capacity_units = 10
