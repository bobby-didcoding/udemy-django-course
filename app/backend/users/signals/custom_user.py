# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from ecommerce.models import Customer, Cart


User = get_user_model()

@receiver(post_save, sender=User, weak=False)
def create_ecommerce_objects(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user = instance)
        Cart.objects.create(user = instance)