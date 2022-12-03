import csv
import random
import string

from ecommerce.products.models import Category, Colour, Media, Product, Size, SubProduct


class SampleData:
    def __init__(self) -> None:
        self.sizes = []
        self.categories = {}
        self.subCategories = {}
        self.colors = {}
        self.products = []
        self.subproducts = []

        self.usages = {}
        self.types = {}
        self.genders = {}
        self.medias = []

        self.colors_order = []
        self.medias_order = []

    def clean_all_data(self):
        Size.objects.all().delete()
        Category.objects.all().delete()
        Colour.objects.all().delete()
        Product.objects.all().delete()
        SubProduct.objects.all().delete()
        Media.objects.all().delete()

    def create_products(self):
        with open("scripts/fashion.csv") as csvfile:
            fashion = csv.reader(csvfile)
            next(fashion, None)  # skip the headers
            for row in fashion:
                if row[1] not in self.genders:
                    self.genders[row[1]] = row[1][0]
                if row[2] not in self.categories:
                    self.categories[row[2]] = Category.objects.create(name=row[2])
                if row[3] not in self.subCategories:
                    self.subCategories[row[3]] = Category.objects.create(
                        name=row[3], parent=self.categories[row[2]]
                    )
                """ if(row[4] not in types):
                    types[row[4]] = Type.objects.create(name=row[4]) """
                if row[5] not in self.colors:
                    self.colors[row[5]] = Colour.objects.create(name=row[5])
                if row[6] not in self.usages:
                    self.usages[row[6]] = row[6]
                product = Product(
                    name=row[7],
                    genre=self.genders[row[1]],
                    category=self.subCategories[row[3]],
                    # type=row[4],
                    usage=self.usages[row[6]],
                    # image_url = row[9]
                )
                self.medias_order.append(row[9])
                self.colors_order.append(self.colors[row[5]])
                self.products.append(product)

        Product.objects.bulk_create(self.products)
        self.products = Product.objects.all()

    def set_products_details(self):
        for i in range(len(self.products)):
            self.create_variantes(self.products[i], self.colors_order[i])
            self.medias.append(
                Media(url=self.medias_order[i], product=self.products[i])
            )
        SubProduct.objects.bulk_create(self.subproducts)
        Media.objects.bulk_create(self.medias)

    def create_sample_sizes(self):
        self.sizes.append(Size(name="SM"))
        self.sizes.append(Size(name="MD"))
        self.sizes.append(Size(name="LG"))
        self.sizes.append(Size(name="XL"))
        Size.objects.bulk_create(self.sizes)

    def create_variantes(self, product, color):
        for size in Size.objects.all():
            sku = "".join(random.choices(string.ascii_uppercase + string.digits, k=20))
            self.subproducts.append(
                SubProduct(
                    SKU=sku,
                    rr_price=0,
                    store_price=0,
                    sale_price=0,
                    product=product,
                    colour=color,
                    size=size,
                )
            )


def run():
    """Product.objects.all().delete()
    Gender.objects.all().delete()
    Category.objects.all().delete()
    SubCategory.objects.all().delete()
    Type.objects.all().delete()
    Usage.objects.all().delete"""
    # Fetch all questions
    sample = SampleData()
    sample.clean_all_data()
    sample.create_products()
    sample.create_sample_sizes()
    sample.set_products_details()
    print(len(sample.products))
    print(len(sample.subproducts))


#    Product.objects.bulk_create(products)
