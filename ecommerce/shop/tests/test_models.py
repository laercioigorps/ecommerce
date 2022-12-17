# import pytest
from ecommerce.products.models import SubProduct

from ..models import ProductDetail


def test_product_with_subproducts_fixture(product_with_many_sub_products):
    count = SubProduct.objects.all().count()
    assert count == 3


def test_product_detail_page_colours_context(product_with_many_sub_products, rf):
    """Tests product get_context has all subproducts colours"""
    product = product_with_many_sub_products
    detail_page = ProductDetail(product=product)
    request = rf.get("/random-page")
    page_context = detail_page.get_context(request=request)
    subproducts = product.subproducts.all()

    assert subproducts[0].colour in page_context["colours"]
    assert subproducts[1].colour in page_context["colours"]
    assert subproducts[2].colour in page_context["colours"]


def test_product_detail_page_context_has_active_colour(
    product_with_many_sub_products, rf
):
    """Tests product get_context has all subproducts colours"""
    product = product_with_many_sub_products
    detail_page = ProductDetail(product=product)
    request = rf.get("/random-page?colour=colour-1")
    page_context = detail_page.get_context(request=request)
    assert page_context["colour"] == "colour-1"


def test_product_detail_contains_price_range(product_with_many_sub_products, rf):
    """Tests product get_context has subproducts min and max price(store_price and sale_price)"""
    product = product_with_many_sub_products
    detail_page = ProductDetail(product=product)
    request = rf.get("/random-page")
    page_context = detail_page.get_context(request=request)

    assert str(page_context["price_range"]["store_price__min"]) == "150.99"
    assert str(page_context["price_range"]["store_price__max"]) == "161.25"

    assert str(page_context["price_range"]["sale_price__min"]) == "120.00"
    assert str(page_context["price_range"]["sale_price__max"]) == "132.00"


def test_product_detail_contains_price_range_for_colour(
    product_with_many_sub_products, rf
):
    """Tests product get_context has subproducts min and max price(store_price and sale_price)"""
    product = product_with_many_sub_products
    detail_page = ProductDetail(product=product)
    request = rf.get("/random-page?colour=colour-1")
    page_context = detail_page.get_context(request=request)

    assert str(page_context["price_range"]["store_price__min"]) == "150.99"
    assert str(page_context["price_range"]["store_price__max"]) == "150.99"

    assert str(page_context["price_range"]["sale_price__min"]) == "120.00"
    assert str(page_context["price_range"]["sale_price__max"]) == "120.00"


def test_product_detail_page_context_with_subproducts_filtered_by_colour(
    product_with_many_sub_products, rf
):
    product = product_with_many_sub_products
    sub_product = product.subproducts.first()
    detail_page = ProductDetail(product=product)
    request = rf.get(f"/random-page?colour={sub_product.colour.name}")
    page_context = detail_page.get_context(request=request)

    assert len(page_context["subproducts"]) == 1
    assert page_context["subproducts"][0].colour.name == "colour-1"
    assert page_context["subproducts"][0].SKU == "XYZ123456"


def test_product_detail_page_context_with_subproducts_filtered_by_colour_name_ignoring_case(
    product_with_many_sub_products, rf
):
    product = product_with_many_sub_products
    detail_page = ProductDetail(product=product)
    request = rf.get("/random-page?colour=Colour-1")
    page_context = detail_page.get_context(request=request)

    assert len(page_context["subproducts"]) == 1
    assert page_context["subproducts"][0].colour.name == "colour-1"
    assert page_context["subproducts"][0].SKU == "XYZ123456"


def test_product_detail_page_context_with_subproduct_when_SKU(
    product_with_many_sub_products, rf
):
    product = product_with_many_sub_products
    detail_page = ProductDetail(product=product)
    request = rf.get("/random-page?colour=Colour-1&sku=XYZ123456")
    page_context = detail_page.get_context(request=request)

    assert "subproduct" in page_context
    assert page_context["subproduct"].SKU == "XYZ123456"
