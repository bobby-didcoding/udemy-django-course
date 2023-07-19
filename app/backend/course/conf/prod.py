from .common import *

from dotenv import load_dotenv
import os
import socket
load_dotenv()

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

PRODUCTION = 1
DEBUG = 0

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
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL}'
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