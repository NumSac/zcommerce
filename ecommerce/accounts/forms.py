# users/forms.py

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "is_company",
            "company_name",
            "vat_number",
            "address",
            "contact_person_name",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "is_company",
            "company_name",
            "vat_number",
            "address",
            "contact_person_name",
        )


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label=("Username"), max_length=254)
    password = forms.CharField(
        label=("Password"), strip=False, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)
        # You can add some customization here. For example, adding classes to your fields:
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )
