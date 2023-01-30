from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from ecommerce.products.models import SubProduct

from .services import ShoppingCartServices

# Create your views here.


class CartPageView(View):
    def get(self, request):
        if "cart" in request.session:
            items_in = SubProduct.objects.in_bulk(request.session["cart"])
            items = []
            for item in items_in:
                items.append(
                    {
                        "item": items_in[item],
                        "quantity": int(request.session["cart"][str(item)]["quantity"]),
                    }
                )
        else:
            items = None
        return render(request, "shop/shopping_cart_page.html", {"items": items})


class ShoppingCartAddItemView(View):
    def post(self, request):
        item = request.POST.get("item")
        quantity = request.POST.get("quantity")
        subproduct = get_object_or_404(SubProduct, pk=item)
        if request.user.is_authenticated:
            shoppingcart = ShoppingCartServices.get_active_or_create(request.user)
            # checks if the item already exists in the cart
            ShoppingCartServices.add_or_update_cart_item(
                shoppingcart, subproduct, quantity
            )
        if "cart" not in request.session:
            request.session["cart"] = {}
        if str(subproduct.id) not in request.session["cart"]:
            request.session["cart"][str(subproduct.id)] = {"quantity": quantity}
        else:
            request.session["cart"][str(subproduct.id)]["quantity"] = str(
                int(request.session["cart"][str(subproduct.id)]["quantity"])
                + int(quantity)
            )
        request.session.modified = True
        return HttpResponseRedirect(reverse("shop:cart_page"))


class ShoppingCartRemoveItemView(View):
    def post(self, request, item):
        subproduct = get_object_or_404(SubProduct, pk=item)
        if (
            "cart" not in request.session
            or str(subproduct.id) not in request.session["cart"]
        ):
            return HttpResponse(status=404)
        else:
            if request.user.is_authenticated:
                shoppingcart = ShoppingCartServices.get_active_or_create(request.user)
                shoppingcart.items.remove(subproduct)
            del request.session["cart"][str(subproduct.id)]
            request.session.modified = True
            return HttpResponseRedirect(reverse("shop:cart_page"))
