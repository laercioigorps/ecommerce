from django.db import models

from ecommerce.models import TimeStampedModel

# Create your models here.


class Brand(TimeStampedModel):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")

    def __str__(self) -> str:
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name


class ProductType(TimeStampedModel):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")

    def __str__(self) -> str:
        return self.name


class Size(TimeStampedModel):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")

    def __str__(self) -> str:
        return self.name


class Colour(TimeStampedModel):
    name = models.CharField(max_length=30)
    description = models.TextField(default="")

    def __str__(self) -> str:
        return self.name


class Product(TimeStampedModel):

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

    def __str__(self) -> str:
        return self.name


class SubProduct(TimeStampedModel):
    SKU = models.CharField(max_length=40, unique=True)
    rr_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    store_price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return "{} - {} - {}".format(
            self.product.name, self.colour.name, self.size.name
        )


class Media(models.Model):
    url = models.CharField(max_length=200)
    description = models.TextField(default="")
    alt_text = models.TextField(default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
