from django.db import models

from ecommerce.models import TimeStampedModel

# Create your models here.


class Brand(TimeStampedModel):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")


class Category(TimeStampedModel):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)


class ProductType(TimeStampedModel):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")


class Size(TimeStampedModel):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")


class Colour(TimeStampedModel):
    name = models.CharField(max_length=30)
    description = models.TextField(default="")


class Product(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)


class SubProduct(TimeStampedModel):
    SKU = models.CharField(max_length=40, unique=True)
    rr_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    store_price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)


class Media(models.Model):
    url = models.CharField(max_length=140)
    description = models.TextField(default="")
    alt_text = models.TextField(default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
