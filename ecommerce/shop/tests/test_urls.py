from django.urls import resolve, reverse

from ..views import ShoppingCartAddItemView


def test_add_item_to_shopping_cart_url():
    resolve("/shop/add-to-cart/").view_name == "shop:add_to_cart"
    resolve(reverse("shop:add_to_cart")).func == ShoppingCartAddItemView.as_view()
