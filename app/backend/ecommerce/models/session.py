# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from decimal import *

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from utils.abstracts import ExternalID, Model
from utils.fields.enums import SessionMode, SessionStatus


# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.models import Customer, SessionItem

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
from django_enumfield.enum import EnumField


class Session(
    ExternalID, 
    Model
    ):

    customer = models.ForeignKey(
        Customer, 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL,
        verbose_name=_('session customer'),
        related_name="session_customer")
    
    session_items = models.ManyToManyField(
        SessionItem, 
        verbose_name=_('session items'),
        blank=True, 
        related_name="session_session_items"
        )


    session_mode = EnumField(SessionMode, blank=True, null=True, verbose_name=_('session mode'), default=SessionMode.payment)
    session_status = EnumField(SessionStatus, blank=True, null=True, verbose_name=_('session status'), default=SessionStatus.open)

    @property
    def empty_cart(self):
        cart = self.customer.user.cart_user
        for p in cart.products.all():
            cart.products.remove(p)
        cart.save()