# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
import logging

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from utils.decorators import suspendingreceiver

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.models import Price

logger = logging.getLogger(__name__)

@suspendingreceiver(post_save, sender=Price, weak=False)
def create_price(sender, instance, created, **kwargs):
    if created:
        '''
        Create a stripe price
        '''
        pass