from django.urls import path

from .views import ShoppingCartView

app_name = "shop"

urlpatterns = [
    path("/add-to-cart/", view=ShoppingCartView.as_view(), name="add_to_cart")
]
