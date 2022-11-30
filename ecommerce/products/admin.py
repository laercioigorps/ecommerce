from django.contrib import admin

from .models import Brand, Category, Colour, Media, Product, Size, SubProduct

# Register your models here.

admin.site.register(Product)
admin.site.register(SubProduct)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Colour)
admin.site.register(Media)
