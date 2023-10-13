from django.contrib.auth.models import User, Permission
from django.contrib.auth.management import create_permissions
from django.test.client import Client
from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from string import ascii_letters
from random import choices

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers

# Create your tests here.
class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2,3)
        self.assertEqual(result, 5)

class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete


    def test_create_product(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "199.99",
                "description": "A good table",
                "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )

class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)

class ProductsListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json'
    ]

    def test_products(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = self.client.get(reverse("shopapp:products_list"))
        # products = Product.objects.filter(archived=False).all()
        # products_ = response.context["products"]
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)
        self.assertQuerySetEqual(
            qs = Product.objects.filter(archived=False).all(),
            values = (p.pk for p in response.context["products"]),
            transform = lambda p: p.pk
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')

class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="test_user", password="qwerty")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_view(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_autheticated(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.client.logout()

        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="testuser", password="Qazwsxedc12#")
        permission = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address="ul.Rabotashaja, 13",
            promocode="TEST",
            user=self.user,
        )
        self.product = Product.objects.create(name="Best product")
        self.order.products.add(self.product)

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = self.client.get(reverse("shopapp:order_details", kwargs={"pk": self.order.pk}))
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context["object"].pk, self.order.pk)

class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_get_products_view(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = self.client.get(
            reverse("shopapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data
        )