from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View
from injector import inject


from services.aws.dynamodb_admin_service import DynamoDbAdminServiceController
from services.aws.dynamodb_initialize import DynamoDBInitialize


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
        dynamodb_initializer: DynamoDBInitialize,
        **kwargs
    ):
        self.dynamodb_service = dynamodb_service
        self.dynamodb_initializer = dynamodb_initializer
        super().__init__(**kwargs)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        try:
            # Check if tables are already created
            tables_created = self.dynamodb_initializer.are_tables_created()

            # Fetch DynamoDB metadata using the injected service
            db_metadata = self.dynamodb_service.get_db_metadata()

            context = {
                "db_metadata": db_metadata,
                "tables_created": tables_created,
            }
            return render(request, "aws/manage.html", context)

        except Exception as e:
            context = {"error_message": str(e)}
            print(e)
            return render(request, "aws/error.html", context)

    def post(self, request, *args, **kwargs):
        try:
            # Initialize DynamoDB tables using the db_initialize method
            self.dynamodb_initializer.create_tables()

            context = {"message": "Tables created"}

        except Exception as e:
            context = {"error_message": str(e)}

        return render(request, "aws/manage.html", context)


def dynamodb_fetch_all_entries(request):
    return
