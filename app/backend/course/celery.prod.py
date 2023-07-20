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

 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course.conf.prod')
app = Celery('course')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "send_account_summary_to_support": {
        "task": "tasks.tasks.send_account_summary_to_support",
        "schedule": timedelta(hours=24),
    },
}
 
app.autodiscover_tasks()
