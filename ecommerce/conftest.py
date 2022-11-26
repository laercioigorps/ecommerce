import pytest

from ecommerce.products.models import (
    Brand,
    Category,
    Colour,
    Product,
    ProductType,
    Size,
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
def product(db, category) -> Product:
    return Product.objects.create(
        name="newProduct", description="someDescription", category=category
    )
