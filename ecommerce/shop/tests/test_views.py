import pytest

from ecommerce.shop.views import ShoppingCartView


def test_add_invalid_item_to_shopping_cart_view(user, rf):
    request = rf.post("/random/", {"item": 999, "quantity": 2})
    request.user = user

    view = ShoppingCartView.as_view()
    with pytest.raises(Exception):
        view(request)


def test_add_item_to_shopping_cart_with_valid_user_view(user, rf, subProduct):
    request = rf.post("/random/", {"item": subProduct.id, "quantity": 2})
    request.user = user
    view = ShoppingCartView.as_view()
    response = view(request)
    cart_item_count = subProduct.shoppingcartitem_set.count()
    cart_item = subProduct.shoppingcartitem_set.first()

    assert response.status_code == 200
    assert cart_item_count == 1
    assert cart_item.quantity == 2
    assert cart_item.cart.owner == user
