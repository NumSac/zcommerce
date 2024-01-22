from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View
from injector import inject


from services.aws.dynamodb_service_controller import DynamoDbAdminServiceController


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
