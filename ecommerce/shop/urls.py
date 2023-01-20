from django.urls import path

from .views import ShoppingCartAddItemView

app_name = "shop"

urlpatterns = [
    path("add-to-cart/", view=ShoppingCartAddItemView.as_view(), name="add_to_cart")
]
