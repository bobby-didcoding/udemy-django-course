# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from utils.abstracts import TimeStampedModel, Model, ActivatorModel

class Contact(
    TimeStampedModel,
    ActivatorModel, 
    Model):

    class Meta:
        verbose_name_plural = "Contacts"

    name = models.CharField(_('name'),max_length=100)
    email = models.EmailField(_('email'))
    message = models.TextField(_('message'),max_length=1000)

    def __str__(self):
        return f'{self.name}'