# import pytest
from ecommerce.products.models import SubProduct

from ..models import ProductDetail


def test_product_with_subproducts_fixture(product_with_many_sub_products):
    count = SubProduct.objects.all().count()
    assert count == 3


def test_product_detail_page_colours_context(product_with_many_sub_products, rf):
    product = product_with_many_sub_products
    detail_page = ProductDetail(product=product)
    request = rf.get("/random-page")
    page_context = detail_page.get_context(request=request)
    subproducts = product.subproducts.all()

    assert subproducts[0].colour in page_context["colours"]
    assert subproducts[1].colour in page_context["colours"]
    assert subproducts[2].colour in page_context["colours"]


def test_product_detail_contains_price_range(product_with_many_sub_products, rf):
    product = product_with_many_sub_products
    detail_page = ProductDetail(product=product)
    request = rf.get("/random-page")
    page_context = detail_page.get_context(request=request)

    assert str(page_context["price_range"]["store_price__min"]) == "150.99"
    assert str(page_context["price_range"]["store_price__max"]) == "161.25"

    assert str(page_context["price_range"]["sale_price__min"]) == "120.00"
    assert str(page_context["price_range"]["sale_price__max"]) == "132.00"
