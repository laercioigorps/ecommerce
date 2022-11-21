import pytest

from ecommerce.products.models import Brand, Category, Colour, ProductType, Size


@pytest.mark.django_db
def test_count_brand_equals_0():
    brand_count = Brand.objects.all().count()
    assert brand_count == 0


@pytest.mark.django_db
def test_create_brand():
    Brand.objects.create(name="SomeBrand", description="some description")
    brand_count = Brand.objects.all().count()
    assert brand_count == 1


@pytest.mark.django_db
def test_create_category():
    Category.objects.create(name="someCategory", description="some description")
    catogories_count = Category.objects.all().count()
    assert catogories_count == 1


@pytest.mark.django_db
def test_create_category_with_parent_category():
    parent = Category.objects.create(
        name="father", description="some father description"
    )
    category = Category.objects.create(
        name="children", description="some child description", parent=parent
    )
    catogories_count = Category.objects.all().count()
    assert catogories_count == 2
    assert category.parent.id == parent.id


@pytest.mark.django_db
def test_create_type():
    ProductType.objects.create(name="some", description="some description")
    product_type_count = ProductType.objects.all().count()
    assert product_type_count == 1


@pytest.mark.django_db
def test_create_product_size():
    Size.objects.create(name="XG", description="someDescription")
    sizes_count = Size.objects.all().count()
    assert sizes_count == 1


@pytest.mark.django_db
def test_create_product_color():
    Colour.objects.create(name="someColour", description="some colour description")
    colours_count = Colour.objects.all().count()
    assert colours_count == 1
