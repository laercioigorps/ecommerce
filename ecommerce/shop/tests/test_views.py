import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from ecommerce.products.tests.factories import SubProductFactory
from ecommerce.shop.models import ShoppingCart
from ecommerce.shop.views import ShoppingCartAddItemView, ShoppingCartRemoveItemView

from ..services import ShoppingCartServices


@pytest.mark.django_db
def test_shopping_cart_page_with_logged_user(user, client, subProduct):
    cart = ShoppingCartServices.get_active_or_create(user)
    ShoppingCartServices.add_or_update_cart_item(cart=cart, item=subProduct, quantity=3)

    client.force_login(user)
    response = client.get(reverse("shop:cart_page"))
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/shopping_cart_page.html")
    assert len(response.context["items"]) == 1
    assert response.context["items"][0].item.id == subProduct.id
    assert response.context["items"][0].quantity == 3


def test_add_invalid_item_to_shopping_cart_view(user, rf):
    request = rf.post("/random/", {"item": 999, "quantity": 2})
    request.user = user

    view = ShoppingCartAddItemView.as_view()
    with pytest.raises(Exception):
        view(request)


def test_add_item_to_shopping_cart_with_valid_user_view(user, rf, subProduct):
    request = rf.post("/random/", {"item": subProduct.id, "quantity": 2})
    request.user = user
    view = ShoppingCartAddItemView.as_view()
    response = view(request)
    cart_item_count = subProduct.shoppingcartitem_set.count()
    cart_item = subProduct.shoppingcartitem_set.first()

    assert response.status_code == 200
    assert cart_item_count == 1
    assert cart_item.quantity == 2
    assert cart_item.cart.owner == user


def test_add_two_items_to_same_shopping_cart(user, rf):
    item1 = SubProductFactory()
    item2 = SubProductFactory()

    view = ShoppingCartAddItemView.as_view()

    # add first item
    request = rf.post("/random/", {"item": item1.id, "quantity": 2})
    request.user = user
    response = view(request)
    # add second item
    request = rf.post("/random/", {"item": item2.id, "quantity": 3})
    request.user = user
    response = view(request)

    shopping_cart_count = ShoppingCart.objects.all().count()
    shopping_cart = ShoppingCart.objects.first()
    shopping_cart_items = shopping_cart.items.all()

    assert response.status_code == 200
    assert shopping_cart_count == 1
    assert shopping_cart_items.count() == 2
    assert shopping_cart_items[0].id == item1.id
    assert shopping_cart_items[1].id == item2.id


def test_add_same_item_twice_to_shopping_cart(user, rf, subProduct):
    view = ShoppingCartAddItemView.as_view()

    # add first item
    request = rf.post("/random/", {"item": subProduct.id, "quantity": 2})
    request.user = user
    response = view(request)
    # add second item
    request = rf.post("/random/", {"item": subProduct.id, "quantity": 3})
    request.user = user
    response = view(request)

    shopping_cart = ShoppingCart.objects.first()
    shopping_cart_items = shopping_cart.items.all()
    shopping_cart_item = shopping_cart.shoppingcartitem_set.first()

    assert response.status_code == 200
    assert shopping_cart_items.count() == 1
    assert shopping_cart_item.item == subProduct
    assert shopping_cart_item.quantity == 5


def test_delete_shopping_cart_item(user, rf, subProduct):
    view = ShoppingCartAddItemView.as_view()
    # add first item
    request = rf.post("/random/", {"item": subProduct.id, "quantity": 2})
    request.user = user
    response = view(request)
    # add second item
    view = ShoppingCartRemoveItemView.as_view()
    request = rf.post("/random/")
    request.user = user
    response = view(request, subProduct.id)

    shopping_cart = ShoppingCart.objects.first()
    shopping_cart_items = shopping_cart.items.all()

    assert response.status_code == 200
    assert shopping_cart_items.count() == 0


def test_delete_invelid_shopping_cart_item(user, rf, subProduct):
    # add second item
    view = ShoppingCartRemoveItemView.as_view()
    request = rf.post("/random/")
    request.user = user
    response = view(request, subProduct.id)

    shopping_cart = ShoppingCart.objects.first()
    shopping_cart_items = shopping_cart.items.all()

    assert response.status_code == 404
    assert shopping_cart_items.count() == 0
