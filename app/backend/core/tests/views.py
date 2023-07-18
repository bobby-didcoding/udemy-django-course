# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.test import TestCase
from django.test.client import Client

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from core.views import (
    HomeView,
)

class HomeViewTestCase(TestCase):
    """
    Test suite for HomeView
    """

    def setUp(self):
        
        self.client = Client()

    def test_home_view_get_request(self):
        client = self.client
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

