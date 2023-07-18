# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.test.utils import override_settings
from django.contrib.auth import get_user_model
from django.test import TestCase

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from users.tests import BaseTestCustomUser


# --------------------------------------------------------------
# App Party imports
# --------------------------------------------------------------
from ecommerce.models import (
    Cart,
    Customer,
    Price,
    Product,
)

User = get_user_model()

@override_settings(SUSPEND_SIGNALS=True)
class BaseEcommerceTest(TestCase, BaseTestCustomUser):

    def setUp(self):
        self.user = self.get_test_active_user()

        self.customer = Customer.objects.create(user = self.user)
        self.cart = Cart.objects.create(customer = self.customer)

        self.price, created = Price.objects.get_or_create(amount=10.0)
        self.product, created = Product.objects.get_or_create(
            title="Test product",
            description="Test description",
            price = self.price,
            )
        
        self.cart.products.add(self.product)
        self.cart.save()


class PriceTestCase(BaseEcommerceTest):
    """
    Test suite for Price
    """


    def test_price_creation(self):
        obj = self.price
        self.assertTrue(isinstance(obj, Price))
        self.assertEqual(obj.status, 1)
        self.assertEqual(obj.amount, 10.0)

    def test_price_stripe_amount_method(self):
        obj = self.price
        self.assertEqual(obj.stripe_amount, 1000)


class ProductTestCase(BaseEcommerceTest):
    """
    Test suite for Product
    """

    def test_product_creation(self):
        obj = self.product
        price = self.price
        self.assertTrue(isinstance(obj, Product))
        self.assertEqual(obj.status, 1)
        self.assertTrue(price == obj.price, True)
        self.assertEqual(obj.status, 1)
        self.assertEqual(obj.slug, 'test-product')

    def test_product_get_absolute_url_method(self):
        obj = self.product
        self.assertEqual(obj.get_absolute_url(), '/product/test-product/')


class CustomerTestCase(BaseEcommerceTest):
    """
    Test suite for Customer
    """

    def test_customer_creation(self):
        obj = self.customer
        self.assertTrue(isinstance(obj, Customer))

        self.assertEqual(obj.__str__(), "Test Case")
        self.assertEqual(obj.status, 1)


class CartTestCase(BaseEcommerceTest):
    """
    Test suite for Cart
    """

    def test_customer_creation(self):
        obj = self.cart
        product = self.product
        self.assertTrue(isinstance(obj, Cart))
        self.assertEqual(obj.status, 1)
        self.assertTrue(product in obj.products.all(), True)
        self.assertTrue(obj.products.all().count(), 1)

