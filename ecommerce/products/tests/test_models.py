import pytest

from ecommerce.products.models import Brand


@pytest.mark.django_db
def test_count_brand_equals_0():
    brand_count = Brand.objects.all().count()
    assert brand_count == 0


@pytest.mark.django_dbs
def test_create_brand():
    Brand.objects.create(name="SomeBrand", description="some description")
    brand_count = Brand.objects.all().count()
    assert brand_count == 1
