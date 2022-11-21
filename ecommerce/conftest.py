import pytest

from ecommerce.products.models import Brand, Category
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
