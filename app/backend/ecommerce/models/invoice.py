# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from decimal import *

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from utils.abstracts import Model, ExternalID

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.models import  Customer

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
from django_enumfield.enum import EnumField

User = get_user_model()

class Invoice(
    ExternalID,
    Model):

    customer = models.ForeignKey(
        Customer, 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL,
        verbose_name=_('customer'),
        related_name="invoice_customer"
        )

    hosted_invoice_url = models.URLField(blank=True, null=True)
    invoice_pdf = models.URLField(blank=True, null=True)

    





