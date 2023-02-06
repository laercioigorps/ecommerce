from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from ecommerce.products.models import SubProduct
from ecommerce.users.models import Address

from . import paypal_api
from .models import Order, ShoppingCart
from .services import ShoppingCartServices

# Create your views here.


def get_cart_summary(request):
    items = []
    if "cart" in request.session:
        items_in = SubProduct.objects.in_bulk(request.session["cart"])

        for item in items_in:
            items.append(
                {
                    "item": items_in[item],
                    "quantity": int(request.session["cart"][str(item)]["quantity"]),
                }
            )
    shipping = 5
    subtotal = 0
    for item in items:
        subtotal += item["item"].sale_price * int(item["quantity"])
    total = subtotal + shipping
    return {
        "items": items,
        "shipping": shipping,
        "subtotal": subtotal,
        "total": total,
    }


class CartPageView(View):
    def get(self, request):
        return render(
            request,
            "shop/shopping_cart_page.html",
            context=get_cart_summary(request),
        )


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


class SelectAddressView(LoginRequiredMixin, View):
    def get(self, request):
        address_id = request.GET.get("address", None)
        print(address_id)
        print("------------------------------------------iisisisis")
        if address_id:
            return HttpResponseRedirect(
                reverse("shop:checkout", kwargs={"address": address_id})
            )
        addresses = request.user.address_set.all()
        return render(request, "shop/select_address.html", {"addresses": addresses})


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request, address):
        try:
            address = request.user.address_set.get(pk=address)
        except Address.DoesNotExist:
            return HttpResponseRedirect(reverse("shop:select_address"))

        details = get_cart_summary(request)
        details["address"] = address
        details["client_id"] = paypal_api.CLIENT_ID
        details["client_token"] = paypal_api.generateClientToken()
        return render(request, "shop/checkout.html", context=details)


class CreateOrderView(View):
    def post(self, request, address):
        address = get_object_or_404(Address, pk=address)
        sumary = get_cart_summary(request)
        response = paypal_api.create_order(sumary["total"])
        return HttpResponse(response)


class CaptureOrderView(View):
    def post(self, request, address, order_id):
        address = get_object_or_404(Address, pk=address)
        sumary = get_cart_summary(request)
        response = paypal_api.capture_order(order_id)
        response_json = response.json()
        cart = ShoppingCart.objects.create(owner=request.user, is_active=False)
        for item in sumary["items"]:
            ShoppingCartServices.add_or_update_cart_item(
                cart, item["item"], item["quantity"]
            )
        if response_json["status"] in Order.Statuses:
            Order.objects.create(
                owner=request.user,
                status=response_json["status"],
                total=sumary["total"],
                subtotal=sumary["subtotal"],
                shipping=sumary["shipping"],
                shipping_address=str(address),
                cart=cart,
            )
            del request.session["cart"]
        else:
            return HttpResponse(status=400)
        return HttpResponse(response)


class ListOrderView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(owner=request.user)
        return render(request, "users/list_orders.html", context={"orders": orders})


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        if order.owner != request.user:
            return HttpResponse("You can not access this resource", status=404)
        return render(request, "users/order_detail.html", {"order": order})
