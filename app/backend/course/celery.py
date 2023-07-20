# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
import os
from datetime import timedelta

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.conf import settings

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
from celery import Celery
from celery.schedules import crontab

 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course.conf.dev')
app = Celery('course')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    # "some_task": {
    #     "task": "tasks.tasks.some_task",
    #     "schedule": timedelta(minutes=5),
    # },

}
 
app.autodiscover_tasks()
