from typing import Any
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from injector import inject


from services.aws.dynamodb_service_controller import DynamoDbServiceController


@staff_member_required
def aws_info_view(request):
    aws_status_data = {}
    return render(request, "aws/info.html", {})


class DynamoDbInfoView(View):
    @inject
    def __init__(self, dynamodb_service: DynamoDbServiceController, **kwargs):
        self.dynamodb_service = dynamodb_service
        super().__init__(**kwargs)

    @staff_member_required
    async def get(self, request, *args, **kwargs):
        try:
            # Fetch DynamoDB metadata using the injected service
            db_metadata = await self.dynamodb_service.get_db_metadata()

            context = {"db_metadata": db_metadata}
            return render(request, "aws/info.html", context)

        except Exception as e:
            context = {"error_message": str(e)}
            return render(request, "aws/error.html", context)


class DynamoDbManageView(View):
    @inject
    def __init__(self, dynamodb_service: DynamoDbServiceController, **kwargs):
        self.dynamodb_service = dynamodb_service
        super().__init__(**kwargs)

    @staff_member_required
    async def get(self, request, *args, **kwargs):
        try:
            # Fetch DynamoDB metadata using the injected service
            db_metadata = await self.dynamodb_service.get_db_metadata()

            context = {"db_metadata": db_metadata}
            return render(request, "aws/info.html", context)

        except Exception as e:
            context = {"error_message": str(e)}
            return render(request, "aws/error.html", context)


@staff_member_required
def aws_manage_view(request):
    return render(request, "aws/manage.html", {})
