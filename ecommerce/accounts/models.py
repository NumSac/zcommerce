from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from ecommerce.constants import (
    IS_REGISTERED,
    CAN_PUBLISH_PRODUCTS,
    CAN_PROCESS_ORDERS,
    CAN_USE_CLIENT_CHAT,
    CAN_BACKUP_ITEMS,
    CAN_PROMOTE_PRODUCTS,
    CAN_USE_ANALYTICS,
    CAN_REQUEST_HELPDESK_BOT,
)

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
    class Meta:
        verbose_name_plural = "companies"

    company_profile = models.OneToOneField(
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

    @property
    def registration_number(self):
        owner_instance = self.owner.first()  # Get the owner if it exists
        if owner_instance:
            return owner_instance.registration_number
        return None

    def __str__(self):
        return self.company_name


### CustomUser model with a ForeignKey to Company ###
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


# Create Proxy models for representing different subscription permissions
class BaseSubscription(CustomUser):
    class Meta:
        proxy = True
        permissions = [
            (IS_REGISTERED, "Has registered a company"),
            (CAN_PUBLISH_PRODUCTS, "Can publish products"),
            (CAN_PROCESS_ORDERS, "Can process orders"),
        ]


class SimpleSubscription(BaseSubscription):
    class Meta(BaseSubscription.Meta):
        proxy = True
        permissions = [
            (CAN_USE_CLIENT_CHAT, "Can use client chat"),
            (CAN_BACKUP_ITEMS, "Can backup items"),
        ]


class MediumSubscription(SimpleSubscription):
    class Meta(SimpleSubscription.Meta):
        proxy = True
        permissions = [(CAN_PROMOTE_PRODUCTS, "Can promote products")]


class PremiumSubscription(MediumSubscription):
    class Meta(MediumSubscription.Meta):
        proxy = True
        permissions = [
            (CAN_USE_ANALYTICS, "Can use analytics"),
            (CAN_REQUEST_HELPDESK_BOT, "Can request helpdesk bot"),
        ]
