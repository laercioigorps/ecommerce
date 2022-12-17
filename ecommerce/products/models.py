from django.db import models
from django.db.models import Max, Min
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

# Create your models here.


@register_snippet
class Brand(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


@register_snippet
class Size(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


@register_snippet
class Colour(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Product(ClusterableModel, index.Indexed):

    GENRE_CHOICES = [
        ("G", "Girl"),
        ("B", "Boys"),
        ("W", "Women"),
        ("M", "Men"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, null=True)
    usage = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldRowPanel(
            [
                FieldPanel("category"),
                FieldPanel("brand"),
            ]
        ),
        FieldRowPanel(
            [
                FieldPanel("genre"),
                FieldPanel("usage"),
            ]
        ),
        InlinePanel("product_medias", heading="Medias", label="Media"),
        InlinePanel("subproducts", heading="Sub Products", label="Sub Product"),
    ]

    search_fields = [
        index.SearchField("name", partial_match=True),
    ]

    def __str__(self) -> str:
        return self.name

    def get_price_range(self, colour_name=None):
        subproducts = self.subproducts.all()
        if colour_name:
            subproducts = subproducts.filter(colour__name__iexact=colour_name)
        price_range = subproducts.aggregate(
            Max("sale_price"), Min("sale_price"), Max("store_price"), Min("store_price")
        )
        if price_range["sale_price__min"] is None:
            return None
        return price_range

    def get_colours(self):
        dif_colours = Colour.objects.filter(subproduct__product__pk=self.pk).distinct()
        return dif_colours


class ProductFilterSet(WagtailFilterSet):
    class Meta:
        model = Product
        fields = {
            "category__name": ["icontains"],
            "brand__name": ["icontains"],
            "genre": ["icontains"],
            "usage": ["icontains"],
        }


class SubProduct(models.Model):
    SKU = models.CharField(max_length=40, unique=True)
    rr_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    store_price = models.DecimalField(max_digits=6, decimal_places=2)
    product = ParentalKey(Product, on_delete=models.CASCADE, related_name="subproducts")
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("SKU"),
        FieldRowPanel(
            [
                FieldPanel("rr_price"),
                FieldPanel("sale_price"),
                FieldPanel("store_price"),
            ]
        ),
        FieldRowPanel(
            [
                FieldPanel("colour"),
                FieldPanel("size"),
            ]
        ),
    ]

    def __str__(self) -> str:
        return "{} - {} - {}".format(
            self.product.name, self.colour.name, self.size.name
        )


class Media(models.Model):
    url = models.CharField(max_length=200)
    description = models.TextField(default="")
    alt_text = models.TextField(default="")
    product = ParentalKey(
        Product, on_delete=models.CASCADE, related_name="product_medias"
    )
