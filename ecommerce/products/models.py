from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")


class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
