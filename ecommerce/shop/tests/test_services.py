import pytest

from ..models import ShoppingCart
from ..services import ShoppingCartServices


@pytest.mark.django_db
def test_get_active_shopping_cart_or_create_should_create(user):
    shopping_cart_count = ShoppingCart.objects.count()
    assert shopping_cart_count == 0
    shopping_cart = ShoppingCartServices.get_active_or_create(owner=user)
    shopping_cart_count = ShoppingCart.objects.count()
    assert shopping_cart_count == 1
    assert shopping_cart.is_active


@pytest.mark.django_db
def test_get_active_shopping_cart_or_create_should_not_create(user):
    shopping_cart = ShoppingCartServices.get_active_or_create(owner=user)
    shopping_cart_count = ShoppingCart.objects.count()
    assert shopping_cart_count == 1

    shopping_cart = ShoppingCartServices.get_active_or_create(owner=user)
    shopping_cart_count = ShoppingCart.objects.count()
    assert shopping_cart.owner == user
    assert shopping_cart_count == 1


@pytest.mark.django_db
def test_add_or_update_cart_item_should_add(user, subProduct):
    shopping_cart = ShoppingCartServices.get_active_or_create(owner=user)
    assert shopping_cart.items.count() == 0
    ShoppingCartServices.add_or_update_cart_item(shopping_cart, subProduct, 3)
    shopping_cart_item = shopping_cart.shoppingcartitem_set.get(item=subProduct)
    assert shopping_cart.items.count() == 1
    assert shopping_cart_item.quantity == 3


@pytest.mark.django_db
def test_add_or_update_cart_item_should_update(user, subProduct):
    shopping_cart = ShoppingCartServices.get_active_or_create(owner=user)
    ShoppingCartServices.add_or_update_cart_item(shopping_cart, subProduct, 3)
    ShoppingCartServices.add_or_update_cart_item(shopping_cart, subProduct, 3)

    shopping_cart_item = shopping_cart.shoppingcartitem_set.get(item=subProduct)
    assert shopping_cart.items.count() == 1
    assert shopping_cart_item.quantity == 6
