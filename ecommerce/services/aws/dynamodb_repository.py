from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class DynamoDBRepository:
    def __init__(self, model_class):
        self.model_class = model_class

    def get_item(self, primary_key):
        try:
            item = self.model_class.get(primary_key)
            return item
        except self.model_class.DoesNotExist:
            return None

    def put_item(self, item_data):
        item = self.model_class(**item_data)
        item.save()

    def update_item(self, item, attributes_to_update):
        for attr, value in attributes_to_update.items():
            setattr(item, attr, value)
        item.save()

    def delete_item(self, item):
        item.delete()

    def query_items(self, index_name=None, **query_kwargs):
        if index_name:
            return list(self.model_class.query(index_name, **query_kwargs))
        else:
            return list(self.model_class.scan(**query_kwargs))

    def scan_items(self, **scan_kwargs):
        return list(self.model_class.scan(**scan_kwargs))
