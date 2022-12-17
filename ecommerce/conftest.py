import pytest

from ecommerce.products.models import (
    Brand,
    Category,
    Colour,
    Media,
    Product,
    ProductType,
    Size,
    SubProduct,
)
from ecommerce.users.models import User
from ecommerce.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def category(db) -> Category:
    return Category.objects.create(name="someName", description="some description")


@pytest.fixture
def brand(db) -> Brand:
    return Brand.objects.create(name="someBrand", description="some description")


@pytest.fixture
def colour(db) -> Colour:
    return Colour.objects.create(
        name="someColour", description="some colour description"
    )


@pytest.fixture
def size(db) -> Size:
    return Size.objects.create(name="sizeName", description="size description")


@pytest.fixture
def productType(db) -> ProductType:
    return ProductType.objects.create(
        name="typeName", description="description of some type"
    )


@pytest.fixture
def product(db, category, brand) -> Product:
    return Product.objects.create(
        name="newProduct", description="someDescription", category=category, brand=brand
    )


@pytest.fixture
def subProduct(db, product, colour, size) -> SubProduct:
    return SubProduct.objects.create(
        SKU="XYZ123456",
        rr_price=99.90,
        store_price=150.99,
        sale_price=120.00,
        product=product,
        colour=colour,
        size=size,
    )


@pytest.fixture
def media(db, product):
    return Media.objects.create(
        url="heeps://someurl.com/123",
        description="some image description",
        alt_text="what is happening in the image",
        product=product,
    )


@pytest.fixture
def product_with_many_sub_products(db, product):
    colour1 = Colour.objects.create(name="colour-1", description="")
    colour2 = Colour.objects.create(name="colour-2", description="")
    colour3 = Colour.objects.create(name="colour-3", description="")

    size1 = Size.objects.create(name="MD")
    size2 = Size.objects.create(name="LG")
    size3 = Size.objects.create(name="XL")
    subProducts = []
    subProducts.append(
        SubProduct(
            SKU="XYZ123456",
            rr_price=99.90,
            store_price=150.99,
            sale_price=120.00,
            product=product,
            colour=colour1,
            size=size1,
        )
    )
    subProducts.append(
        SubProduct(
            SKU="XYZ123455",
            rr_price=90.90,
            store_price=160.25,
            sale_price=130.00,
            product=product,
            colour=colour2,
            size=size2,
        )
    )
    subProducts.append(
        SubProduct(
            SKU="XYZ123454",
            rr_price=100.90,
            store_price=161.25,
            sale_price=132.00,
            product=product,
            colour=colour3,
            size=size3,
        )
    )

    SubProduct.objects.bulk_create(subProducts)

    return product
