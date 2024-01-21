from django.urls import path

from .views import *

app_name = "aws"

urlpatterns = [
    path("", aws_info_view, name="info"),
    path("manage/", aws_manage_view, name="manage"),
]
