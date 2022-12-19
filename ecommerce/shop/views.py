# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from ecommerce.products.models import SubProduct

from .models import ShoppingCart

# Create your views here.


class ShoppingCartView(View):
    def post(self, request):
        item = request.POST.get("item")
        quantity = request.POST.get("quantity")

        subproduct = get_object_or_404(SubProduct, pk=item)
        carts = ShoppingCart.objects.filter(owner=request.user).filter(is_active=True)
        if not carts:
            shoppingcart = ShoppingCart.objects.create(owner=request.user)
        else:
            shoppingcart = carts.first()
        # checks if the item already exists in the cart
        is_cart_item = shoppingcart.items.all().filter(pk=subproduct.id).exists()
        if not is_cart_item:
            # add item
            shoppingcart.items.add(
                subproduct, through_defaults={"quantity": int(quantity)}
            )
        else:
            # updates the item quantity
            shopping_cart_item = shoppingcart.shoppingcartitem_set.get(item=subproduct)
            shopping_cart_item.quantity += int(quantity)
            shopping_cart_item.save()
        return HttpResponse(status=200)
