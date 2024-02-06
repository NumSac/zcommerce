from django.db import models
from django.utils import timezone
from django.utils.text import slugify


import datetime

# Create your models here.

from django.db import models

from ecommerce.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
    )
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    listed = models.BooleanField(default=False)
    mark_for_sync = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug

            # Ensure the slug is unique
            num = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{num}"
                num += 1

        super().save(*args, **kwargs)

    class Meta:
        ordering = ("title", "created_at")
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.title
