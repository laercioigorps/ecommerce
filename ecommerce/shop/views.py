# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from ecommerce.products.models import SubProduct

from .services import ShoppingCartServices

# Create your views here.


class ShoppingCartView(View):
    def post(self, request):
        item = request.POST.get("item")
        quantity = request.POST.get("quantity")

        subproduct = get_object_or_404(SubProduct, pk=item)
        shoppingcart = ShoppingCartServices.get_active_or_create(request.user)
        # checks if the item already exists in the cart
        ShoppingCartServices.add_or_update_cart_item(shoppingcart, subproduct, quantity)
        return HttpResponse(status=200)
