from django.urls import path

from ecommerce.users.views import user_detail_view, user_redirect_view, user_update_view

from .views import CreateAddressView, EditAddressView, ListCreateView

app_name = "users"
urlpatterns = [
    path("address/", view=ListCreateView.as_view(), name="list_create_address"),
    path("address/add/", view=CreateAddressView.as_view(), name="create_address"),
    path(
        "address/<int:address_id>/edit/",
        view=EditAddressView.as_view(),
        name="edit_address",
    ),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
