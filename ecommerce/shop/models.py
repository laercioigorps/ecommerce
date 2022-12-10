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
