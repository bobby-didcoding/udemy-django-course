# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
import logging

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.db.models.signals import post_save
from django.conf import settings

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from utils.decorators import suspendingreceiver

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.models import Invoice


logger = logging.getLogger(__name__)

@suspendingreceiver(post_save, sender=Invoice, weak=False)
def create_invoice(sender, instance, created, **kwargs):
    if created:
        '''
        Create a stripe invoice
        '''
        pass