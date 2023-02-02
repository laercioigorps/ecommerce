from django.urls import path

from .views import (
    CartPageView,
    SelectAddressView,
    ShoppingCartAddItemView,
    ShoppingCartRemoveItemView,
)

app_name = "shop"

urlpatterns = [
    path("add-to-cart/", view=ShoppingCartAddItemView.as_view(), name="add_to_cart"),
    path(
        "remove-from-cart/<int:item>",
        view=ShoppingCartRemoveItemView.as_view(),
        name="remove_from_cart",
    ),
    path(
        "cart/",
        view=CartPageView.as_view(),
        name="cart_page",
    ),
    path(
        "cart/select-address/",
        view=SelectAddressView.as_view(),
        name="select_address",
    ),
]
