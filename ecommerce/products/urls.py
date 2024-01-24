from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("edit/<slug:slug>/", views.EditView.as_view(), name="edit"),
    path("delete/<slug:slug>/", views.DeleteView.as_view(), name="delete"),
    path("sync/", views.SyncView.as_view(), name="sync"),
]
