from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse, request

from django.urls import reverse_lazy
from django.views import generic

from .models import Product, Category
from .forms import ProductCreationForm, ProductDeletionForm, ProductEditationForm

# Create your views here.


class IndexView(generic.ListView):
    template_name = "products/index.html"
    context_object_name = "product_list"

    def get_queryset(self) -> QuerySet[Any]:
        return Product.objects.all()


class CreateView(generic.CreateView):
    model = Product
    success_url = reverse_lazy("index")
    form_class = ProductCreationForm
    template_name = "products/create.html"
    context_object_name = "product"


class DetailView(generic.DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"


class EditView(generic.UpdateView):
    model = Product
    template_name = "products/edit.html"
    form_class = ProductEditationForm
    context_object_name = "product"


class DeleteView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy("index")
    template_name = "products/delete.html"
    context_object_name = "product"
