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
