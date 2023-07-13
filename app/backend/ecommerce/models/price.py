# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.utils.translation import gettext_lazy as _
from django.db import models

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from utils.abstracts import Model,ExternalID


class Price(
    ExternalID,
    Model):
    
    interval_count = models.IntegerField(default=1, null=True, blank=True)
