from django.core.management import BaseCommand
from shopapp.models import Order, Product
from django.contrib.auth.models import User

class Command(BaseCommand):
    """
    Update order
    """
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        order = Order.objects.first()
        if not order:
            self.stdout.write("no order found")
            return
        products = Product.objects.all()
        for product in products:
            order.products.add(product)

        order.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully added products {order.products.all()} to order {order}"))
