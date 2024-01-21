from django.shortcuts import render

# Create your views here.
# users/views.py

from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserLoginForm


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")  # Redirect to login page after signup
    template_name = "registration/signup.html"


class LoginView(generic.CreateView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy("index")  # Redirect to login page after signup
    template_name = "registration/login.html"
