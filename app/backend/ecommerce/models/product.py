# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.utils.translation import gettext_lazy as _
from django.db import models



# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from utils.abstracts import Model, ExternalID

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.models import Price

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
from django_extensions.db.models import TitleSlugDescriptionModel


class Product(
    TitleSlugDescriptionModel,
    ExternalID,
    Model):

    price = models.ForeignKey(Price, blank=True, null=True, on_delete=models.SET_NULL, related_name="product_price")

    def __Str__(self):
        return f'{self.title}'