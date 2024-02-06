from django.urls import path

from .views import SyncView, DetailView

app_name = "sync"

urlpatterns = [
    path("", SyncView.as_view(), name="index"),
    path("detail/<str:product_id>", view=DetailView.as_view(), name="detail"),
]
