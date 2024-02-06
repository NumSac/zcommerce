from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import (
    CustomUserCreationForm,
    CustomUserLoginForm,
)
from django.conf import settings

from .forms import CustomUserCreationForm, CompanyProfileForm, CompanyForm


# Add permissions after User created registered a company
def add_user_to_group(
    request,
    user_id,
):
    user = get_object_or_404(settings.CUSTOM_AUTH_USER, pk=user_id)


# Generic Views for login in signup
class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class LoginView(generic.CreateView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy("index")
    template_name = "registration/login.html"

class CompanyProfileView(View):
    template_name = "registration/create_or_edit_company.html"

    def get(self, request):
        user = request.user

        if user.company:
            company_profile = user.company.company_profile
            company = user.company
            company_profile_form = CompanyProfileForm(instance=company_profile)
            company_form = CompanyForm(instance=company)
            is_editing = True
        else:
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
            company.save(commit=False)
            user.is_company = True
            user.company = company
            user.save()
            return redirect("accounts:profile")

        context = {
            "company_profile_form": company_profile_form,
            "company_form": company_form,
            "is_editing": False,
        }
        messages.success(request, "Success!.")
        return render(request, self.template_name, context)
