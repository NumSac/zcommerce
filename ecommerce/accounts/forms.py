# users/forms.py

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from .models import CustomUser, Company, CompanyProfile


class CompanyEditForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "company_name",
            "vat_number",
            "address",
            "contact_person_name",
        ]


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ["company_description", "company_background_image"]


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "company_name",
            "vat_number",
            "address",
            "contact_person_name",
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "vat_number": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "contact_person_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
        )


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label=("Username"), max_length=254)
    password = forms.CharField(
        label=("Password"), strip=False, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )
