from ecommerce.products.models import Category, Colour, Product, Size, SubProduct


def clean_all_data():
    Size.objects.all().delete()
    Category.objects.all().delete()
    Category.objects.all().delete()
    Colour.objects.all().delete()
    Product.objects.all().delete()
    SubProduct.objects.all().delete()


def run():
    clean_all_data()
