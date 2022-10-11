import stripe
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...models import Product, Price


class Command(BaseCommand):
    help = "Sync up the stripe products with local database"

    def handle(self, **options):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        products = stripe.Product.list(active=True)
        for product in products:
            for price in stripe.Price.list(product=product.id):
                with transaction.atomic():
                    product, _ = Product.objects.get_or_create(
                        image_url=product.images[0],
                        defaults={
                            "name": product.name,
                            "stripe_product_id": product.id,
                        },
                    )
                    Price.objects.get_or_create(
                        product=product,
                        stripe_price_id=price.id,
                        defaults={
                            "price": price.unit_amount,
                            "active": price.active,
                        },
                    )
