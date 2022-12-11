from datetime import date

import pytest
from django.db import IntegrityError

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

    def test_brand_name_is_object_name(self, brand):
        assert brand.name == str(brand)


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

    def test_category_name_is_object_name(self, category):
        assert category.name == str(category)


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

    def test_productType_name_is_object_name(self, productType):
        assert productType.name == str(productType)


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

    def test_size_name_is_object_name(self, size):
        assert size.name == str(size)


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

    def test_colour_name_is_object_name(self, colour):
        assert colour.name == str(colour)


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

    def test_product_brand(self, product):
        assert isinstance(product.brand, Brand)

    @pytest.mark.django_db
    def test_product_genre_girl(self, product):
        product.genre = "G"
        product.save()
        copy = Product.objects.get(pk=product.id)
        assert copy.get_genre_display() == "Girl"

    @pytest.mark.django_db
    def test_product_genre_boys(self, product):
        product.genre = "B"
        product.save()
        copy = Product.objects.get(pk=product.id)
        assert copy.get_genre_display() == "Boys"

    @pytest.mark.django_db
    def test_product_genre_women(self, product):
        product.genre = "W"
        product.save()
        copy = Product.objects.get(pk=product.id)
        assert copy.get_genre_display() == "Women"

    @pytest.mark.django_db
    def test_product_genre_men(self, product):
        product.genre = "M"
        product.save()
        copy = Product.objects.get(pk=product.id)
        assert copy.get_genre_display() == "Men"

    @pytest.mark.django_db
    def test_product_usage(self, product):
        product.usage = "Casual"
        product.save()
        copy = Product.objects.get(pk=product.id)
        assert copy.usage == "Casual"

    def test_product_name_is_object_name(self, product):
        assert product.name == str(product)

    @pytest.mark.django_db
    def test_product_price_range_none_without_subproducts(self, product):
        assert product.get_price_range() is None

    @pytest.mark.django_db
    def test_product_price_range_min_and_max(self, product):
        SubProduct.objects.create(
            SKU="qwe", rr_price=20, store_price=25, sale_price=22, product=product
        )
        SubProduct.objects.create(
            SKU="ewq", rr_price=19, store_price=24, sale_price=20, product=product
        )
        price_range = product.get_price_range()
        assert price_range["store_price__min"] == 24
        assert price_range["store_price__max"] == 25
        assert price_range["sale_price__min"] == 20
        assert price_range["sale_price__max"] == 22

    @pytest.mark.django_db
    def test_product_all_colors_report(self, product, colour, size):
        product1 = SubProduct.objects.create(
            SKU="qwe",
            rr_price=20,
            store_price=25,
            sale_price=22,
            product=product,
            colour=colour,
            size=size,
        )
        colour2 = Colour.objects.create(name="new")
        product2 = SubProduct.objects.create(
            SKU="ewq",
            rr_price=19,
            store_price=24,
            sale_price=20,
            product=product,
            colour=colour2,
            size=size,
        )
        colours = product.get_colours()
        assert len(colours) == 2
        assert colours[0]["colour"].name == colour.name
        assert colours[1]["colour"].name == colour2.name

        assert len(colours[0]["subproducts"]) == 1
        assert colours[0]["subproducts"][0].SKU == product1.SKU

        assert len(colours[1]["subproducts"]) == 1
        assert colours[1]["subproducts"][0].SKU == product2.SKU


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

    def test_subProduct_fixture(self, subProduct):
        assert isinstance(subProduct, SubProduct)

    def test_subProduct_is_timestamped(self, subProduct):
        assertIsTimestamped(subProduct)

    @pytest.mark.django_db(transaction=True)
    def test_subProduc_SKU_is_unique(self, subProduct):
        subProductsCount = SubProduct.objects.all().count()
        assert subProductsCount == 1

        with pytest.raises(IntegrityError):
            SubProduct.objects.create(
                SKU=subProduct.SKU,
                rr_price=99.90,
                store_price=150.99,
                sale_price=120.00,
                product=subProduct.product,
            )
        subProductsCount = SubProduct.objects.all().count()
        assert subProductsCount == 1

    def test_subProduct_has_colour(self, subProduct):
        assert isinstance(subProduct, SubProduct)
        assert subProduct.colour in Colour.objects.all()

    def test_subProduct_has_size(self, subProduct):
        assert subProduct.size in Size.objects.all()

    def test_subproduct_name_is_product_name_color_and_size(self, subProduct):
        pattert = "{} - {} - {}".format(
            subProduct.product.name,
            subProduct.colour.name,
            subProduct.size.name,
        )
        assert pattert == str(subProduct)


class TestProductMedia:
    def test_create_media(self, product):
        media_count = Media.objects.all().count()
        assert media_count == 0
        Media.objects.create(
            url="heeps://someurl.com/123",
            description="some image description",
            alt_text="what is happening in the image",
            product=product,
        )
        media_count = Media.objects.all().count()
        assert media_count == 1

        product_media_count = product.product_medias.all().count()
        assert product_media_count == 1

    def test_media_fixture(self, media):
        assert isinstance(media, Media)
