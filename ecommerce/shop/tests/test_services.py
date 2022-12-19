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
