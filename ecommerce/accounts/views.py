from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import (
    CustomUserCreationForm,
    CustomUserLoginForm,
)

from .forms import CustomUserCreationForm, CompanyProfileForm, CompanyForm


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")  # Redirect to login page after signup
    template_name = "registration/signup.html"


class LoginView(generic.CreateView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy("index")  # Redirect to login page after signup
    template_name = "registration/login.html"


class CompanyProfileView(View):
    template_name = "registration/create_or_edit_company.html"

    def get(self, request):
        user = request.user

        if user.company:
            # User already has a company and profile, edit them
            company_profile = user.company.company_profile
            company = user.company
            company_profile_form = CompanyProfileForm(instance=company_profile)
            company_form = CompanyForm(instance=company)
            is_editing = True
        else:
            # User doesn't have a company and profile, create them
            company_profile_form = CompanyProfileForm()
            company_form = CompanyForm()
            is_editing = False

        context = {
            "company_profile_form": company_profile_form,
            "company_form": company_form,
            "is_editing": is_editing,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        company_profile_form = CompanyProfileForm(request.POST, request.FILES)
        company_form = CompanyForm(request.POST)

        if company_profile_form.is_valid() and company_form.is_valid():
            company_profile = company_profile_form.save()
            company = company_form.save(commit=False)
            company.company_profile = company_profile
            company.save()
            user.is_company = True
            user.company = company
            user.save()
            return redirect("accounts:profile")

        context = {
            "company_profile_form": company_profile_form,
            "company_form": company_form,
            "is_editing": False,
        }
        return render(request, self.template_name, context)
