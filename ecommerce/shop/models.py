from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
        pages = ProductDetail.objects.live().public().filter(product__genre=self.genre)
        min_price = request.GET.get("minamount", None)
        max_price = request.GET.get("maxamount", None)
        sizes = request.GET.getlist("size")
        colours = request.GET.getlist("colour")
        if min_price:
            pages = pages.filter(
                product__subproducts__sale_price__gte=min_price
            ).distinct()
        if max_price:
            pages = pages.filter(
                product__subproducts__sale_price__lte=max_price
            ).distinct()
        if sizes:
            pages = pages.filter(product__subproducts__size__name__in=sizes)
        if colours:
            pages = pages.filter(product__subproducts__colour__name__in=colours)
        paginator = Paginator(pages, 12)
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)
        context["pages"] = posts
        context["filtered_colours"] = colours
        context["filtered_sizes"] = sizes
        context["filtered_maxprice"] = max_price
        context["filtered_minprice"] = min_price
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
