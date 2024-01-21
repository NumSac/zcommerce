from ecommerce.accounts.models import CustomUser
from ecommerce.products.models import Product, Category


def serialize_product_to_dynamodb_dto(product_instance: Product):
    return {
        "ProductId": str(product_instance.id),  # DynamoDB prefers string identifiers
        "Name": product_instance.name,
        "Description": product_instance.description,
        "Price": str(product_instance.price),  # Convert Decimal to string
        "Available": product_instance.available,
        "Stock": product_instance.stock,
        # Add other fields as necessary
    }


def serialize_company_to_dynamodb_dto(company_instance: CustomUser):
    return {
        "registration_number": company_instance.registration_number,
        "name": company_instance.name,
        "vat_number": company_instance.vat_number,
        "address": company_instance.address,
        "contact_person_name": company_instance.contact_person_name,
    }
