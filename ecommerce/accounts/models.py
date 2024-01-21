# users/models.py

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User Auth object
class CustomUser(AbstractUser):
    # Add additional fields here if you need
    age = models.PositiveIntegerField(null=True, blank=True)

    is_company = models.BooleanField(
        default=False, help_text=_("Designates whether this user is a company account.")
    )
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The legal name of the company."),
    )
    registration_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_("The official registration number of the company."),
    )
    vat_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_("The VAT number of the company."),
    )
    address = models.TextField(
        blank=True, null=True, help_text=_("The registered address of the company.")
    )
    contact_person_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The name of the primary contact person for the company."),
    )

    def __str__(self):
        return self.email if self.email else self.username


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
