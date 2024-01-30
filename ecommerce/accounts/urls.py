from django.urls import path

from .views import SignUpView, LoginView, CompanyProfileView

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),  # Custom signuop view
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", CompanyProfileView.as_view(), name="profile"),
]
