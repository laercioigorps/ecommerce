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
        shoppingcart = ShoppingCart.objects.create(owner=request.user)
        shoppingcart.items.add(subproduct, through_defaults={"quantity": int(quantity)})
        return HttpResponse(status=200)
