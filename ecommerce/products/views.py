from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import redirect, render

from uuid import uuid4
from injector import inject

from services.aws.models.product_model import ProductRepository, ProductSerializer

from .models import Product
from .forms import ProductCreationForm, ProductEditationForm

# Create your views here.


class IndexView(generic.ListView):
    template_name = "products/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        queryset = Product.objects.filter(owner=self.request.user)
        name_query = self.request.GET.get("title", "")
        min_price = self.request.GET.get("min_price", None)
        max_price = self.request.GET.get("max_price", None)

        if name_query:
            queryset = queryset.filter(name__icontains=name_query)

        # Filter by price range if min_price and/or max_price are provided
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Product
    form_class = ProductCreationForm
    template_name = "products/create.html"
    success_url = reverse_lazy("products:index")
    check_ownership = True

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailView(generic.DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"
    check_ownership = True


class EditView(generic.UpdateView):
    model = Product
    success_url = reverse_lazy("products:index")
    template_name = "products/edit.html"
    form_class = ProductEditationForm
    context_object_name = "product"
    check_ownership = True


class DeleteView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy("products:index")
    template_name = "products/delete.html"
    context_object_name = "product"
    check_ownership = True
