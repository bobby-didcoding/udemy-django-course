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

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from core.models import Team, Tag



def blog_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/policies/<slug>/<filename>
    return os.path.join('blogs', str(instance.slug), filename)

class Blog(
    TimeStampedModel,
    TitleSlugDescriptionModel,
    ActivatorModel,
    Model
    ):
    '''
    Our Blog model. This is used to create policy pages such as cookie and privacy
    '''

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ['id']

    author = models.ForeignKey(Team, blank=True, null=True, on_delete=models.SET_NULL, related_name="blog_author")
    tags = models.ManyToManyField(Tag, blank=True, related_name="blog_tags")

    image = models.ImageField(_('image'),upload_to=blog_directory_path, default="default_blog_image.jpg")

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f"/blog/{self.slug}"
