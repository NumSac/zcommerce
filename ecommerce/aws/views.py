from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View
from injector import inject


from services.aws.dynamodb_admin_service import DynamoDbAdminServiceController
from services.aws.dynamodb_initialize import (
    UsersTable,
    CompanyTable,
    ProductsTable,
    ShoppingCartTable,
)


class DynamoDbInfoView(UserPassesTestMixin, View):
    @inject
    def __init__(self, dynamodb_service: DynamoDbAdminServiceController, **kwargs):
        self.dynamodb_service = dynamodb_service
        super().__init__(**kwargs)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        try:
            # Fetch DynamoDB metadata using the injected service
            db_metadata = self.dynamodb_service.get_db_metadata()

            context = {"db_metadata": db_metadata}
            return render(request, "aws/info.html", context)

        except Exception as e:
            context = {"error_message": str(e)}
            return render(request, "aws/error.html", context)


class DynamoDbManageView(UserPassesTestMixin, View):
    @inject
    def __init__(
        self,
        dynamodb_service: DynamoDbAdminServiceController,
        users_table: UsersTable,
        products_table: ProductsTable,
        shopping_cart_table: ShoppingCartTable,
        company_table: CompanyTable,
        **kwargs
    ):
        self.dynamodb_service = dynamodb_service
        self.users_table = users_table
        self.products_table = products_table
        self.shopping_cart_table = shopping_cart_table
        self.company_table = company_table
        super().__init__(**kwargs)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        try:
            # Fetch DynamoDB metadata using the injected service and compare them to local database entries
            db_metadata = self.dynamodb_service.get_db_metadata()

            context = {"db_metadata": db_metadata}
            return render(request, "aws/manage.html", context)

        except Exception as e:
            context = {"error_message": str(e)}
            return render(request, "aws/error.html", context)

    def post(self, request, *args, **kwargs):
        try:
            # Try to initiate the DynamoDB schema
            products_table_created = self.products_table.create_table()
            shopping_cart_table_created = self.shopping_cart_table.create_table()
            company_table_created = self.company_table.create_table()

            context = {
                "products_table_created": products_table_created,
                "shopping_cart_table_created": shopping_cart_table_created,
                "company_table_created": company_table_created,
            }

            return render(request, "aws/manage.html", context)
        except Exception as e:
            context = {"error_message": str(e)}
            return render(request, "aws/error.html", context)
