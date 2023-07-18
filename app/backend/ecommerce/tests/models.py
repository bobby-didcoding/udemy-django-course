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
    Session,
    SessionItem
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

        self.session_item = SessionItem.objects.create(
            customer=self.customer,
            product = self.product,
            price = self.price
        )

        self.session = Session.objects.create(
            customer = self.customer,
        )
        self.session.session_items.add(self.session_item)
        self.session.save()


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

class SessionItemTestCase(BaseEcommerceTest):
    """
    Test suite for SessionItem
    """
    def test_session_item_creation(self):
        obj = self.session_item
        self.assertTrue(isinstance(obj, SessionItem))
        self.assertEqual(obj.status, 1)
        self.assertEqual(obj.price.amount, 10.0)


class SessionTestCase(BaseEcommerceTest):
    """
    Test suite for Session
    """
    def test_session_creation(self):
        obj = self.session
        self.assertTrue(isinstance(obj, Session))
        self.assertEqual(obj.status, 1)

    def test_session_empty_cart_method(self):
        obj = self.session
        cart = self.cart
        self.assertEqual(cart.products.all().count(), 1)
        obj.empty_cart
        self.assertEqual(cart.products.all().count(), 0)