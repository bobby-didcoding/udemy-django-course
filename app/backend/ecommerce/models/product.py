# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
import os

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


def product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/products/<slug>/<filename>
    return os.path.join('products', str(instance.slug), filename)

class Product(
    TitleSlugDescriptionModel,
    ExternalID,
    Model):

    price = models.ForeignKey(Price, blank=True, null=True, on_delete=models.SET_NULL, related_name="product_price")
    image = models.ImageField(_('image'),upload_to=product_directory_path, default="default_image.jpg")

    def __Str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return f'/product/{self.slug}/'