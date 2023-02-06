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


class GenrePage(Page):
    genre = models.CharField(max_length=20, choices=Product.GENRE_CHOICES)

    content_panels = Page.content_panels + [
        FieldPanel("genre"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["pages"] = ProductDetail.objects.filter(product__genre=self.genre)
        return context


class ShoppingCart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(SubProduct, through="ShoppingCartItem")
    is_active = models.BooleanField(default=True)


class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    item = models.ForeignKey(SubProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    class Statuses(models.TextChoices):
        CREATED = "CREATED"
        SAVED = "SAVED"
        APPROVED = "APPROVED"
        VOIDED = "VOIDED"
        COMPLETED = "COMPLETED"
        PAYER_ACTION_REQUIRED = "PAYER_ACTION_REQUIRED"

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2)
    shipping = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=25, choices=Statuses.choices, default=Statuses.CREATED
    )
    shipping_address = models.CharField(max_length=150)
