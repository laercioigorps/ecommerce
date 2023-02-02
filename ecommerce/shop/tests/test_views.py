import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed

from ecommerce.products.tests.factories import SubProductFactory
from ecommerce.shop.models import ShoppingCart


@pytest.mark.django_db
def test_shopping_cart_page_with_logged_user(user, client, subProduct):
    client.force_login(user)
    session = client.session
    session["cart"] = {
        str(subProduct.id): {"quantity": "3"},
    }
    session.save()

    response = client.get(reverse("shop:cart_page"))
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/shopping_cart_page.html")
    assert len(response.context["items"]) == 1
    assert response.context["items"][0]["item"].id == subProduct.id
    assert response.context["items"][0]["quantity"] == 3


@pytest.mark.django_db
def test_shopping_cart_page_with_anonymous_user(client, subProduct):

    session = client.session
    session["cart"] = {
        str(subProduct.id): {"quantity": "3"},
    }
    session.save()
    response = client.get(reverse("shop:cart_page"))
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/shopping_cart_page.html")
    assert len(response.context["items"]) == 1
    assert response.context["items"][0]["item"].id == subProduct.id
    assert response.context["items"][0]["quantity"] == 3


@pytest.mark.django_db
def test_shopping_cart_page_sub_total_and_total_with_shipping(client):

    item1 = SubProductFactory(sale_price=10)
    item2 = SubProductFactory(sale_price=5)

    session = client.session
    session["cart"] = {
        str(item1.id): {"quantity": "3"},
        str(item2.id): {"quantity": "5"},
    }
    session.save()

    response = client.get(reverse("shop:cart_page"))
    assert response.status_code == 200
    assert len(response.context["items"]) == 2
    assert response.context["subtotal"] == 55
    assert response.context["shipping"] == 5
    assert response.context["total"] == 60


@pytest.mark.django_db
def test_add_invalid_item_to_shopping_cart_view(client):
    response = client.post(reverse("shop:add_to_cart"), {"item": 999, "quantity": 2})
    assert response.status_code == 404


@pytest.mark.django_db
def test_add_item_to_shopping_cart_with_valid_user_view(user, client, subProduct):
    client.force_login(user)
    response = client.post(
        reverse("shop:add_to_cart"), {"item": subProduct.id, "quantity": 2}
    )
    cart_item_count = subProduct.shoppingcartitem_set.count()
    cart_item = subProduct.shoppingcartitem_set.first()

    assertRedirects(response, reverse("shop:cart_page"))
    assert cart_item_count == 1
    assert cart_item.quantity == 2
    assert cart_item.cart.owner == user


@pytest.mark.django_db
def test_add_two_items_to_same_shopping_cart(user, client):
    client.force_login(user)
    item1 = SubProductFactory()
    item2 = SubProductFactory()

    # add first item
    client.post(reverse("shop:add_to_cart"), {"item": item1.id, "quantity": 2})
    # add second item
    client.post(reverse("shop:add_to_cart"), {"item": item2.id, "quantity": 3})

    shopping_cart_count = ShoppingCart.objects.all().count()
    shopping_cart = ShoppingCart.objects.first()
    shopping_cart_items = shopping_cart.items.all()

    assert shopping_cart_count == 1
    assert shopping_cart_items.count() == 2
    assert shopping_cart_items[0].id == item1.id
    assert shopping_cart_items[1].id == item2.id


@pytest.mark.django_db
def test_add_same_item_twice_to_shopping_cart(user, client, subProduct):
    client.force_login(user)
    # add first item
    client.post(reverse("shop:add_to_cart"), {"item": subProduct.id, "quantity": 2})
    # add second item
    client.post(reverse("shop:add_to_cart"), {"item": subProduct.id, "quantity": 3})

    shopping_cart = ShoppingCart.objects.first()
    shopping_cart_items = shopping_cart.items.all()
    shopping_cart_item = shopping_cart.shoppingcartitem_set.first()

    assert shopping_cart_items.count() == 1
    assert shopping_cart_item.item == subProduct
    assert shopping_cart_item.quantity == 5


@pytest.mark.django_db
def test_delete_shopping_cart_item(user, client, subProduct):
    client.force_login(user)
    # add first item
    response = client.post(
        reverse("shop:add_to_cart"), {"item": subProduct.id, "quantity": 2}
    )
    # add second item
    response = client.post(reverse("shop:remove_from_cart", args=[subProduct.id]))

    shopping_cart = ShoppingCart.objects.first()
    shopping_cart_items = shopping_cart.items.all()

    assert response.status_code == 302
    assert shopping_cart_items.count() == 0


@pytest.mark.django_db
def test_delete_item_from_shopping_cart_with_valid_user_view_redirects_to_cart_page(
    user, client, subProduct
):
    client.force_login(user)
    # add item
    response = client.post(
        reverse("shop:add_to_cart"), {"item": subProduct.id, "quantity": 2}
    )
    # remove item

    response = client.post(
        reverse("shop:remove_from_cart", kwargs={"item": subProduct.id}),
    )
    assertRedirects(response, reverse("shop:cart_page"))


@pytest.mark.django_db
def test_delete_invalid_shopping_cart_item(user, client, subProduct):
    # add second item
    client.force_login(user)
    response = client.post(
        reverse("shop:remove_from_cart", kwargs={"item": 99}),
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_view_add_item_to_shopping_cart_with_anonymous_user(client, subProduct):
    response = client.post(
        reverse("shop:add_to_cart"), {"item": subProduct.id, "quantity": 2}
    )
    assert response.status_code == 302
    assert client.session["cart"][str(subProduct.id)]["quantity"] == "2"

    # add the same item again
    response = client.post(
        reverse("shop:add_to_cart"), {"item": subProduct.id, "quantity": 1}
    )
    assert response.status_code == 302
    assert client.session["cart"][str(subProduct.id)]["quantity"] == "3"


@pytest.mark.django_db
def test_view_remove_item_to_shopping_cart_with_anonymous_user(client, subProduct):
    # add the same item again
    response = client.post(
        reverse("shop:add_to_cart"), {"item": subProduct.id, "quantity": 1}
    )
    response = client.post(reverse("shop:remove_from_cart", args=[subProduct.id]))
    assert response.status_code == 302
    assert str(subProduct.id) not in client.session["cart"]


@pytest.mark.django_db
def test_select_cart_shipping_address_login_required(client, subProduct):
    # add the same item again
    response = client.get(reverse("shop:select_address"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_select_cart_shipping_address_valid_user(client, user, subProduct):
    client.force_login(user)
    user.address_set.create(
        line_1="line 1 address 1",
        line_2="line 2 address 1",
        city="city 1",
        state="state 1",
        postal_code="postal_code 1",
        country_code="country_code 1",
    )
    user.address_set.create(
        line_1="line 1 address 2",
        line_2="line 2 address 2",
        city="city 2",
        state="state 2",
        postal_code="postal_code 2",
        country_code="country_code 2",
    )
    # add the same item again
    response = client.get(reverse("shop:select_address"))
    assert response.status_code == 200
    assertTemplateUsed(response, "shop/select_address.html")
    assert len(response.context["addresses"]) == 2
    assert response.context["addresses"][0].line_1 == "line 1 address 1"
    assert response.context["addresses"][1].line_1 == "line 1 address 2"
