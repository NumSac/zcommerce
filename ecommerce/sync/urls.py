from django.urls import path

from .views import SyncView

app_name = "sync"

urlpatterns = [path("", SyncView.as_view(), name="index")]
