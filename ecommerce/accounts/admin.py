from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Company, CompanyProfile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = ["registration_number"]
    list_display = [
        "email",
        "username",
        "is_staff",
        "is_company",
        "company",
    ]

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "is_company",
                    "registration_number",
                    "company",
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
                    "registration_number",
                    "company",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Company)
admin.site.register(CompanyProfile)
