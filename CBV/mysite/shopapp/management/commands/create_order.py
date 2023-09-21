from django.core.management import BaseCommand
from shopapp.models import Order
from django.contrib.auth.models import User

class Command(BaseCommand):
    """
    Creates order
    """
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        user = User.objects.get(username="mike")
        order = Order.objects.get_or_create(
            delivery_address= "ul. Puplina, d.8",
            promocode = "SALE123",
            user = user,
        )
        self.stdout.write(f"Order created: {order}")