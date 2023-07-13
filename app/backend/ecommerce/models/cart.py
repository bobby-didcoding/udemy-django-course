# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from decimal import *

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.utils.translation import gettext_lazy as _
from django.db import models

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.models import Customer, Product

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from utils.abstracts import Model



class Cart(Model):

    customer = models.OneToOneField(
        Customer, 
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name="cart_customer")
    
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name="cart_products",
        verbose_name=_('products')
    )

    @property
    def total(self):
        count = 0
        for p in self.products.all():
            count += p.price.amount
        return count
    
    @property
    def stripe_amount(self):
        return int(self.total * 100)
