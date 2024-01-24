from typing import Any
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import render

from injector import inject

from .models import Product
from .forms import ProductCreationForm, ProductEditationForm

from services.aws.dynamodb_user_service import DynamoDbUserServiceController

# Create your views here.


class IndexView(generic.ListView):
    template_name = "products/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        queryset = Product.objects.filter(owner=self.request.user.id)
        name_query = self.request.GET.get("name", "")
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


class SyncView(UserPassesTestMixin, View):
    """
    View for uploading products to store dynamodb
    """

    @inject
    def __init__(
        self, dynamodb_user_service: DynamoDbUserServiceController, **kwargs
    ) -> None:
        self.dynamodb_user_service = dynamodb_user_service
        super().__init__(**kwargs)

    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request, *args, **kwargs):
        try:
            products_to_sync = self.dynamodb_user_service.compare_products_for_sync(
                Product, self.request.user.id
            )

            products_in_store = self.dynamodb_user_service.get_products_for_user(
                self.request.user.id
            )

            context = {
                "products_to_sync": products_to_sync,
                "products_in_store": products_in_store,
            }

            return render(request, "products/sync.html", context)

        except Exception as e:
            context = {"error_message": str(e)}
            return render(request, "error.html", context)

    def post(self, request, *args, **kwargs):
        try:
            self.dynamodb_user_service.upload_or_update_product()

        except Exception as e:
            context = {"error_message": str(e)}
            return render(request, "error.html", context)
