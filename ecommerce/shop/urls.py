from django.urls import path

from .views import (
    CaptureOrderView,
    CartPageView,
    CheckoutView,
    CreateOrderView,
    SelectAddressView,
    ShoppingCartAddItemView,
    ShoppingCartRemoveItemView,
    ThankYouPageView,
)

app_name = "shop"

urlpatterns = [
    path("add-to-cart/", view=ShoppingCartAddItemView.as_view(), name="add_to_cart"),
    path(
        "remove-from-cart/<int:item>",
        view=ShoppingCartRemoveItemView.as_view(),
        name="remove_from_cart",
    ),
    path(
        "cart/",
        view=CartPageView.as_view(),
        name="cart_page",
    ),
    path(
        "cart/select-address/",
        view=SelectAddressView.as_view(),
        name="select_address",
    ),
    path(
        "address/<int:address>/checkout/",
        view=CheckoutView.as_view(),
        name="checkout",
    ),
    path(
        "address/<int:address>/create-order/",
        view=CreateOrderView.as_view(),
        name="create_order",
    ),
    path(
        "address/<int:address>/capture-order/<str:order_id>/",
        view=CaptureOrderView.as_view(),
        name="capture",
    ),
    path(
        "thank-you/",
        view=ThankYouPageView.as_view(),
        name="thank_you",
    ),
]
