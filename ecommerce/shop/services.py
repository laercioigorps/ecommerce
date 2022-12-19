from .models import ShoppingCart


class ShoppingCartServices:
    def get_active_or_create(owner):
        carts = ShoppingCart.objects.filter(owner=owner).filter(is_active=True)
        if not carts:
            shoppingcart = ShoppingCart.objects.create(owner=owner)
        else:
            shoppingcart = carts.first()
        return shoppingcart
