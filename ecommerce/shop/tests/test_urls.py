from django.urls import resolve, reverse

from ..views import ShoppingCartAddItemView, ShoppingCartRemoveItemView


def test_add_item_to_shopping_cart_url():
    resolve("/shop/add-to-cart/").view_name == "shop:add_to_cart"
    resolve(reverse("shop:add_to_cart")).func == ShoppingCartAddItemView.as_view()


def test_remove_item_from_shopping_cart_url():
    resolve("/shop/remove-from-cart/15/").view_name == "shop:remove_from_cart"
    resolve(reverse("shop:add_to_cart")).func == ShoppingCartRemoveItemView.as_view()
