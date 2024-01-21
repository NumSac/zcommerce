# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "is_staff",
        "is_company",
        "company_name",
        "registration_number",
        "vat_number",
        "contact_person_name",
    ]  # Update as needed
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "is_company",
                    "company_name",
                    "registration_number",
                    "vat_number",
                    "address",
                    "contact_person_name",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "is_company",
                    "company_name",
                    "registration_number",
                    "vat_number",
                    "address",
                    "contact_person_name",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
