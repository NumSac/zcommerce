from django.forms import ModelForm
from .models import Product


class ProductCreationForm(ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "available", "stock", "image")


class ProductDeletionForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name"]


class ProductEditationForm(ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "available", "stock", "image")
