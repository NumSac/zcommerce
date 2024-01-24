from django.forms import ModelForm
from .models import Product


from django import forms
from .models import Product


class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "price",
            "available",
            "mark_for_sync",
            "stock",
            "image",
        ]


class ProductEditationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "price",
            "available",
            "mark_for_sync",
            "stock",
            "image",
        ]
