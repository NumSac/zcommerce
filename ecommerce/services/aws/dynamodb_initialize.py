from .models.user_model import User
from .models.company_model import Company
from .models.product_model import Product
from .models.order_model import Order


class DynamoDBInitialize:
    @classmethod
    def create_tables(cls):
        table_classes = [User, Company, Product, Order]

        for table_class in table_classes:
            try:
                table_class.create_table(wait=True)
                print(f"Table '{table_class.Meta.table_name}' has been created.")
            except Exception as err:
                print(f"Failed to create table '{table_class.Meta.table_name}': {err}")

    @classmethod
    def are_tables_created(cls):
        table_classes = [User, Company, Product, Order]

        for table_class in table_classes:
            try:
                # Use the table_class.Meta.table_name to check if the table exists
                if table_class.exists():
                    print(f"Table '{table_class.Meta.table_name}' exists.")
                else:
                    print(f"Table '{table_class.Meta.table_name}' does not exist.")
            except Exception as err:
                print(f"Error checking table '{table_class.Meta.table_name}': {err}")
