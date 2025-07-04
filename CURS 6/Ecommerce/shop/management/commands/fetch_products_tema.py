
## Luati 1 produs si il puneti in DB.
##      (nume, pret, imagine)

## Luati 10 produse si le puneti in DB.


from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from shop.models import Product, Category
import requests
import time
import random


### python manage.py fetch_products_tema
class Command(BaseCommand):
    help = "Fetch product from https://dummyjson.com/products/categories"

    def handle(self, *args, **options):
        BASE_URL = "https://dummyjson.com/"
        URL_PRODUCTS = BASE_URL + "products"

        LIMIT = 100
        SKIP = 100

        response = requests.get(URL_PRODUCTS, {"limit": LIMIT, "skip": SKIP})
        product_list = response.json()["products"]

        for prod_dict in product_list:

            name = prod_dict["title"]
            slug = name.lower().replace(" ", "-")
            description = prod_dict["description"]

            price = prod_dict["price"]

            if Product.objects.filter(name=name, slug=slug, description=description):
                print("Produsul deja exista in baza de date.")
                continue

            image_url = prod_dict['thumbnail']
            image_response = requests.get(image_url)

            image_content = image_response.content

            product = Product(name=name, slug=slug, description=description, price=price)

            category_name = prod_dict["category"]

            category_object = Category.objects.filter(name=category_name.title()).first()

            if category_object:
                product.category = category_object
                print("A gasit categoria.")

            product.image.save(name, ContentFile(image_content))

            product.save()

            time.sleep(random.randint(2, 5))

        print("S-a terminat ...")