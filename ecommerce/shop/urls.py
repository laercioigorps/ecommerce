from django.urls import path

from .views import ShoppingCartAddItemView, ShoppingCartRemoveItemView

app_name = "shop"

urlpatterns = [
    path("add-to-cart/", view=ShoppingCartAddItemView.as_view(), name="add_to_cart"),
    path(
        "remove-from-cart/<int:item>",
        view=ShoppingCartRemoveItemView.as_view(),
        name="remove_from_cart",
    ),
]
