from .models import ShoppingCart


class ShoppingCartServices:
    def get_active_or_create(owner):
        carts = ShoppingCart.objects.filter(owner=owner).filter(is_active=True)
        if not carts:
            shoppingcart = ShoppingCart.objects.create(owner=owner)
        else:
            shoppingcart = carts.first()
        return shoppingcart

    def add_or_update_cart_item(cart, item, quantity):
        is_cart_item = cart.items.all().filter(pk=item.id).exists()
        if not is_cart_item:
            # add item
            cart.items.add(item, through_defaults={"quantity": int(quantity)})
        else:
            # updates the item quantity
            shopping_cart_item = cart.shoppingcartitem_set.get(item=item)
            shopping_cart_item.quantity += int(quantity)
            shopping_cart_item.save()
