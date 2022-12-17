from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from ecommerce.products.models import Product


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
