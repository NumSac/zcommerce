from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid


class CompanyProfile(models.Model):
    # Fields related to the company profile
    company_description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The description for the seller's page"),
    )
    company_background_image = models.ImageField(
        upload_to="products/%Y/%m/%d",
        blank=True,
        null=True,
        help_text=_("The background image for the store seller's page"),
    )


class Company(models.Model):
    company_profile = models.ForeignKey(
        CompanyProfile, on_delete=models.CASCADE, related_name="company"
    )
    # Fields related to the company
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The legal name of the company."),
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
        return self.company_name

    def save(self, *args, **kwargs):
        # Check if a CustomUser with the same registration_number exists
        existing_user = CustomUser.objects.filter(
            registration_number=self.registration_number
        ).first()

        if existing_user:
            # Set the is_company attribute of the related CustomUser to True
            existing_user.is_company = True
            existing_user.save()

        super(Company, self).save(*args, **kwargs)


# CustomUser model with a ForeignKey to Company
class CustomUser(AbstractUser):
    is_company = models.BooleanField(
        default=False, help_text=_("Designates whether this user is a company account.")
    )
    registration_number = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    # Fields related to the user
    email = models.EmailField(unique=True)
    # ... other fields ...
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=True, null=True, related_name="owner"
    )

    def __str__(self):
        return self.email if self.email else self.username


class CustomUserManager(BaseUserManager):
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
