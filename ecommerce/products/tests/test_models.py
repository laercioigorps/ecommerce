from datetime import date

import pytest

from ecommerce.products.models import (
    Brand,
    Category,
    Colour,
    Product,
    ProductType,
    Size,
    SubProduct,
)


def assertIsTimestamped(model):
    today = date.today()
    assert model.created_at.date() == today
    assert model.updated_at.date() == today


class TestBrand:
    @pytest.mark.django_db
    def test_count_brand_equals_0(self):
        brand_count = Brand.objects.all().count()
        assert brand_count == 0

    @pytest.mark.django_db
    def test_create_brand(self):
        Brand.objects.create(name="SomeBrand", description="some description")
        brand_count = Brand.objects.all().count()
        assert brand_count == 1

    def test_brand_has_timestamped_info(self, brand):
        today = date.today()
        assert brand.created_at.date() == today
        assert brand.updated_at.date() == today


class TestCategory:
    @pytest.mark.django_db
    def test_create_category(self):
        Category.objects.create(name="someCategory", description="some description")
        catogories_count = Category.objects.all().count()
        assert catogories_count == 1

    def test_category_has_timestamped_info(self, category):
        today = date.today()
        assert category.created_at.date() == today
        assert category.updated_at.date() == today

    @pytest.mark.django_db
    def test_create_category_with_parent_category(self):
        parent = Category.objects.create(
            name="father", description="some father description"
        )
        category = Category.objects.create(
            name="children", description="some child description", parent=parent
        )
        catogories_count = Category.objects.all().count()
        assert catogories_count == 2
        assert category.parent.id == parent.id

    def test_category_is_timestamped(self, category):
        assertIsTimestamped(category)


class TestProductType:
    def test_Type_fixture_is_valid(self, productType):
        assert isinstance(productType, ProductType)

    @pytest.mark.django_db
    def test_create_type(self):
        ProductType.objects.create(name="some", description="some description")
        product_type_count = ProductType.objects.all().count()
        assert product_type_count == 1

    def test_productType_is_timestamped(self, productType):
        assertIsTimestamped(productType)


class TestProductSize:
    def test_size_fixture_is_valid(self, size):
        assert isinstance(size, Size)

    @pytest.mark.django_db
    def test_create_product_size(self):
        Size.objects.create(name="XG", description="someDescription")
        sizes_count = Size.objects.all().count()
        assert sizes_count == 1

    def test_product_size_is_timestamped(self, size):
        assertIsTimestamped(size)


class TestProductColour:
    @pytest.mark.django_db
    def test_create_product_color(self):
        Colour.objects.create(name="someColour", description="some colour description")
        colours_count = Colour.objects.all().count()
        assert colours_count == 1

    def test_colour_fixture_is_valid(self, colour):
        assert isinstance(colour, Colour)

    def test_colour_is_timestamped(self, colour):
        assertIsTimestamped(colour)


class TestProduct:
    def test_create_product(self, category):
        Product.objects.create(
            name="someProduct", description="SomeProduct Description", category=category
        )
        productCount = Product.objects.all().count()
        assert productCount == 1

    def test_product_fixture(self, product):
        assert isinstance(product, Product)

    def test_product_is_timestamped(self, product):
        assertIsTimestamped(product)


class TestSubProduct:
    def test_create_subProduct(self, product):
        SubProduct.objects.create(
            SKU="XYZ123456",
            rr_price=99.90,
            store_price=150.99,
            sale_price=120.00,
            product=product,
        )
        count = SubProduct.objects.all().count()
        assert count == 1
