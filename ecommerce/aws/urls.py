from django.urls import path

from .views import DynamoDbInfoView, DynamoDbManageView

app_name = "aws"

urlpatterns = [
    path("", DynamoDbInfoView.as_view(), name="info"),
    path("manage/", DynamoDbManageView.as_view(), name="manage"),
]
