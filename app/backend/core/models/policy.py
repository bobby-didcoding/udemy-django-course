# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
import os

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from utils.abstracts import TimeStampedModel, Model, ActivatorModel, TitleSlugDescriptionModel


def policy_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/policies/<slug>/<filename>
    return os.path.join('policies', str(instance.slug), filename)

class Policy(
    TimeStampedModel,
    TitleSlugDescriptionModel,
    ActivatorModel,
    Model
    ):
    '''
    Our Policy model. This is used to create policy pages such as cookie and privacy
    '''

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"
        ordering = ['id']

    image = models.ImageField(_('image'),upload_to=policy_directory_path, default="default_policy_image.jpg")

    effective_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f"/policy/{self.slug}"
