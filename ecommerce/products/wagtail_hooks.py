from wagtail.snippets.models import register_snippet

from .models import Product
from .views import ProductViewSet

register_snippet(Product, viewset=ProductViewSet)
