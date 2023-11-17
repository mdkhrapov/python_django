from typing import Sequence

from django.core.management import BaseCommand
from shopapp.models import Order, Product
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    """
    Creates order
    """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order with products")
        user = User.objects.get(username="mike")
        # products: Sequence[Product] = Product.objects.defer("description", "price", "created_at").all()
        products: Sequence[Product] = Product.objects.only("id").all()
        order, created = Order.objects.get_or_create(
            delivery_address= "ul. Ivanova, d.8",
            promocode = "promo5",
            user = user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Order created: {order}")