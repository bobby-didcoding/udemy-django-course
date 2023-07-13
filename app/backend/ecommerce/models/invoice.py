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
from utils.fields.enums import InvoiceStatus

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.models import  InvoiceItem, Customer

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
 
    invoice_items = models.ManyToManyField(InvoiceItem, blank=True, verbose_name=_("invoice items"))

    charge = models.CharField(max_length=150, blank=True, null=True)

    amount_due = models.IntegerField(default = 0,blank=True, null=True)
    amount_paid = models.IntegerField(default = 0,blank=True, null=True)
    amount_remaining = models.IntegerField(default = 0,blank=True, null=True)
    amount_shipping = models.IntegerField(default = 0,blank=True, null=True)

    application_fee_amount = models.IntegerField(default = 0,blank=True, null=True)
    
    attempt_count = models.IntegerField(default = 0,blank=True, null=True)
    attempted = models.BooleanField(default = False)

    currency = models.CharField(max_length=3, blank=True, null=True)
    invoice_status = EnumField(InvoiceStatus, blank=True, null=True, verbose_name=_('invoice status'))

    subtotal = models.IntegerField(default = 0,blank=True, null=True)
    subtotal_excluding_tax = models.IntegerField(default = 0,blank=True, null=True)
    tax = models.IntegerField(default = 0,blank=True, null=True)
    total = models.IntegerField(default = 0,blank=True, null=True)
    
    total_excluding_tax = models.IntegerField(default = 0,blank=True, null=True)

    period_end = models.DateTimeField(blank=True, null=True)
    period_start = models.DateTimeField( blank=True, null=True)

    schedule_created = models.BooleanField(default=False)

    hosted_invoice_url = models.URLField(blank=True, null=True)
    invoice_pdf = models.URLField(blank=True, null=True)

    





