from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from ecommerce.products.models import Product, SubProduct
from ecommerce.users.models import User


# Create your models here.
class HomePage(Page):
    pass


class ShopPage(Page):
    pass


class ProductDetail(Page):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False)

    content_panels = Page.content_panels + [
        FieldPanel("product"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        colour = request.GET.get("colour")
        sku = request.GET.get("sku")
        if colour:
            context["subproducts"] = self.product.subproducts.filter(
                colour__name__iexact=colour
            )
            context["colour"] = colour
        if sku:
            context["subproduct"] = context["subproducts"].get(SKU=sku)
        context["price_range"] = self.product.get_price_range(colour)
        context["colours"] = self.product.get_colours()
        return context


class ShoppingCartPage(Page):
    def get_context(self, request, *args, **kwargs):
        from .services import ShoppingCartServices

        context = super().get_context(request, *args, **kwargs)
        cart = ShoppingCartServices.get_active_or_create(request.user)
        context["items"] = cart.shoppingcartitem_set.all()
        return context


class ShoppingCart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(SubProduct, through="ShoppingCartItem")
    is_active = models.BooleanField(default=True)


class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    item = models.ForeignKey(SubProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
