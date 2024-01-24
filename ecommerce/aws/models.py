from django.db import models


class DynamoDbTable(models.Model):
    name = models.CharField(max_length=255, unique=True)
    aws_region = models.CharField(max_length=50)
    aws_endpoint_url = models.URLField()
    aws_access_key_id = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "DynamoDB Table"
        verbose_name_plural = "DynamoDB Tables"

    def __str__(self):
        return self.name
