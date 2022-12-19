from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from ..models import Brand, Category, Colour, Product, Size, SubProduct


class BrandFactory(DjangoModelFactory):
    name = Faker("company")
    description = "somedescription"

    class Meta:
        model = Brand


class CategoryFactory(DjangoModelFactory):
    name = Faker("company")
    description = "somedescription"

    class Meta:
        model = Category


class SizeFactory(DjangoModelFactory):
    name = Faker("currency_code")
    description = "somedescription"

    class Meta:
        model = Size


class ColourFactory(DjangoModelFactory):
    name = Faker("color_name")
    description = "somedescription"

    class Meta:
        model = Colour


class ProductFactory(DjangoModelFactory):
    name = Faker("name")
    description = "somedescription"
    category = SubFactory(CategoryFactory)
    brand = SubFactory(BrandFactory)
    genre = "W"
    usage = "Casual"

    class Meta:
        model = Product


class SubProductFactory(DjangoModelFactory):
    SKU = Faker("pystr")
    rr_price = Faker(
        "pydecimal", right_digits=2, positive=True, min_value=100, max_value=110
    )
    sale_price = 110
    store_price = 150
    product = SubFactory(ProductFactory)
    colour = SubFactory(ColourFactory)
    size = SubFactory(SizeFactory)

    class Meta:
        model = SubProduct
