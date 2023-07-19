from .common import *

from dotenv import load_dotenv
import os
import socket
load_dotenv()

PRODUCTION = 1
DEBUG = 0

# --------------------------------------------------------------
# STATICFILES SETTINGS
# --------------------------------------------------------------
STATICFILES_DIRS = [
        os.path.join(BASE_DIR,'static'),
        os.path.join(BASE_DIR,'media'),
        ]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR,'mediafiles')
# --------------------------------------------------------------
# END STATICFILES SETTINGS
# --------------------------------------------------------------