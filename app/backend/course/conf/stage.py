from .common import *

from dotenv import load_dotenv
import os
import socket
load_dotenv()

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

PRODUCTION = 1
DEBUG = 1

# --------------------------------------------------------------
# STATICFILES SETTINGS
# --------------------------------------------------------------
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
    os.path.join(BASE_DIR,'media'),
    ]
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = f"https://{os.environ.get('AWS_S3_ENDPOINT_URL')}"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.{os.environ.get('AWS_S3_ENDPOINT_URL')}"
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = os.environ.get('AWS_LOCATION')
AWS_MEDIA_LOCATION = os.environ.get('AWS_MEDIA_LOCATION')
AWS_DEFAULT_ACL = 'public-read'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIA_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)
# --------------------------------------------------------------
# END STATICFILES SETTINGS
# --------------------------------------------------------------

# --------------------------------------------------------------
# DEBUG TOOLBAR SETTINGS
# --------------------------------------------------------------
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', '10.0.2.2']
# --------------------------------------------------------------
# END DEBUG TOOLBAR SETTINGS
# --------------------------------------------------------------

# --------------------------------------------------------------
# START SENTRY SETTINGS
# --------------------------------------------------------------
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DNS'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
# --------------------------------------------------------------
# END SENTRY SETTINGS
# --------------------------------------------------------------

# --------------------------------------------------------------
# Cache settings
# --------------------------------------------------------------
CACHES = {
        "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'{os.environ.get("CELERY_BROKER")}/0',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
# --------------------------------------------------------------
# END CACHE SETTINGS
# --------------------------------------------------------------
