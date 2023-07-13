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
from ecommerce.models import  Customer, Price


class InvoiceItem(
    ExternalID,
    Model):

    customer = models.ForeignKey(
        Customer, 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL,
        verbose_name=_('customer'),
        related_name='invoiceitem_customer')

    price = models.ForeignKey(Price, verbose_name=_('price'), blank=True, null=True, on_delete=models.CASCADE)

    quantity = models.IntegerField(_("quantity"),default=1, blank=True,null=True)

    amount = models.IntegerField(default=0, blank=True, null=True)
    amount_excluding_tax = models.IntegerField(default=0, blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    period_end = models.DateTimeField(blank=True, null=True)
    period_start = models.DateTimeField( blank=True, null=True)
    unit_amount_excluding_tax = models.IntegerField(default=0, blank=True, null=True)