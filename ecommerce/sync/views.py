from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import redirect, render

from injector import inject
from uuid import uuid4

from services.aws.models.product_model import ProductRepository, ProductSerializer

from products.models import Product

# Create your views here.


class DetailView(TemplateView):
    template_name = "sync/detail.html"


class SyncView(UserPassesTestMixin, View):
    """
    View for uploading products to store dynamodb
    """

    @inject
    def __init__(self, product_repo: ProductRepository, **kwargs) -> None:
        self.product_repo = product_repo
        super().__init__(**kwargs)

    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request, *args, **kwargs):
        try:
            local_product_list = Product.objects.filter(
                owner=self.request.user, mark_for_sync=True
            )
            registration_number = local_product_list.first().owner.registration_number
            # If User has already created products
            if local_product_list.exists():
                # Query DynamoDb per Repository for user products
                dynamodb_products = (
                    self.product_repo.get_products_by_registration_number(
                        str(registration_number)
                    )
                )
                # Create a dictionary of DynamoDB products for efficient lookup
                dynamodb_product_dict = {
                    str(p.product_id): p for p in dynamodb_products
                }
                # Compare products from local db against existing
                products_to_sync = [
                    product
                    for product in local_product_list
                    if product.mark_for_sync and product.pk not in dynamodb_product_dict
                ]
                context = {
                    "products_to_sync": products_to_sync,
                    "products_in_store": dynamodb_products,
                }
            else:
                context = {
                    "products_to_sync": [],
                    "products_in_store": [],
                }
            return render(request, "products/sync.html", context)

        except Exception as e:
            print(e)
            context = {"error_message": str(e)}
            return render(request, "error.html", context)

    def post(self, request, *args, **kwargs):
        try:
            products_to_sync = Product.objects.filter(
                owner=self.request.user, mark_for_sync=True
            )
            if products_to_sync.exists():
                registration_number = products_to_sync.first().owner.registration_number
                product_serializer = ProductSerializer()
                # Provide registration_number to product serializer
                for product in products_to_sync:
                    # Serialize product
                    ser_product = product
                    ser_product.product_id = uuid4()
                    ser_product.registration_number = str(registration_number)
                    serialized_product = product_serializer.dump(ser_product)
                    # Mark product locally as listed
                    product.listed = True
                    product.save()

                    self.product_repo.put_item(serialized_product)

            return redirect("products:sync")

        except Product.DoesNotExist:
            error_message = (
                "Products not found. Make sure you have products marked for sync."
            )
            context = {"error_message": error_message}
            return render(request, "error.html", context)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            raise e
            context = {"error_message": error_message}
            return render(request, "error.html", context)
