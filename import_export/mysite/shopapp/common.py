from csv import DictReader
from io import TextIOWrapper

from shopapp.models import Order

def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)

    orders = list()
    for row in reader:
        order = Order(
            delivery_address=row["delivery_address"],
            promocode=row["promocode"],
            created_at=row["created_at"],
            user_id=row["user"]
        )
        order.save()

        products = list(row["products"].split(","))
        order.products.set(products)

        # orders.append(order)
    # Order.objects.bulk_create(orders)
    return orders
