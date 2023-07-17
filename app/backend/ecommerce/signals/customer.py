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
# App imports
# --------------------------------------------------------------
from ecommerce.models import Customer

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Customer, weak=False)
def create_customer(sender, instance, created, **kwargs):
    if created:
        '''
        Create a stripe customer
        '''
        pass