from django.db import models
from wagtail.snippets.models import register_snippet

# Create your models here.


@register_snippet
class Brand(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


@register_snippet
class Size(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


@register_snippet
class Colour(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


@register_snippet
class Product(models.Model):

    GENRE_CHOICES = [
        ("G", "Girl"),
        ("B", "Boys"),
        ("W", "Women"),
        ("M", "Men"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, null=True)
    usage = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class SubProduct(models.Model):
    SKU = models.CharField(max_length=40, unique=True)
    rr_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    store_price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "{} - {} - {}".format(
            self.product.name, self.colour.name, self.size.name
        )


class Media(models.Model):
    url = models.CharField(max_length=200)
    description = models.TextField(default="")
    alt_text = models.TextField(default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
