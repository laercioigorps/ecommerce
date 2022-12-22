from ecommerce.products.tests.factories import SubProductFactory
from ecommerce.shop.services import ShoppingCartServices

from ..models import ShoppingCartPage


def test_shopping_cart_page_context_has_items_in_cart(user, rf):
    request = rf.get("random/")
    request.user = user
    item1 = SubProductFactory()
    item2 = SubProductFactory()
    cart = ShoppingCartServices.get_active_or_create(user)
    ShoppingCartServices.add_or_update_cart_item(cart, item1, 2)
    ShoppingCartServices.add_or_update_cart_item(cart, item2, 3)

    cart_page = ShoppingCartPage()
    cart_page_context = cart_page.get_context(request=request)
    cart_page_items = cart_page_context["items"]
    assert cart_page_items[0].item == item1
    assert cart_page_items[0].quantity == 2
    assert cart_page_items[1].item == item2
    assert cart_page_items[1].quantity == 3
