import json
from pathlib import Path

from django.core.management.base import BaseCommand

from products.models import Product

class Command(BaseCommand):
    help = 'Adds 10,000 products to the database'

    def handle(self, *args, **options):
        product_filepath = (Path(__file__).parent).joinpath('products.json')

        with open(product_filepath) as f:
            data = json.load(f)
            for product in data[:1000]:
                Product.objects.create(title=product['title'], price=product['price'])

        products_count = Product.objects.count()
        print(f"{products_count:,} products added")
