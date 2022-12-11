# from django.shortcuts import render
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import ProductFilterSet


class ProductViewSet(SnippetViewSet):
    list_display = ["name", "category", "brand", "genre", "usage", UpdatedAtColumn()]
    filterset_class = ProductFilterSet
