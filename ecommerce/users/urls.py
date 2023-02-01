from django.urls import path

from ecommerce.users.views import user_detail_view, user_redirect_view, user_update_view

from .views import ListCreateView

app_name = "users"
urlpatterns = [
    path("address/", view=ListCreateView.as_view(), name="list_create_address"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
