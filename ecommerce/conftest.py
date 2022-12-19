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
from ecommerce.products.tests.factories import (
    BrandFactory,
    CategoryFactory,
    ColourFactory,
    ProductFactory,
    SizeFactory,
    SubProductFactory,
)
from ecommerce.shop.models import ShoppingCart
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
    return CategoryFactory()


@pytest.fixture
def brand(db) -> Brand:
    return BrandFactory()


@pytest.fixture
def colour(db) -> Colour:
    return ColourFactory()


@pytest.fixture
def size(db) -> Size:
    return SizeFactory()


@pytest.fixture
def productType(db) -> ProductType:
    return ProductType.objects.create(
        name="typeName", description="description of some type"
    )


@pytest.fixture
def product(db, category, brand) -> Product:
    return ProductFactory()


@pytest.fixture
def subProduct(db) -> SubProduct:
    return SubProductFactory()


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


@pytest.fixture
def shoppingcart(db, user):
    return ShoppingCart.objects.create(owner=user)
