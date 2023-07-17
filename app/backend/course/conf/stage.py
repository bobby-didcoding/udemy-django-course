from .common import *

from dotenv import load_dotenv
import os
import socket
load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
PRODUCTION = 0
DEBUG = 1

# Application definition
RUN_SERVER_PORT = 8000

# --------------------------------------------------------------
# DATABASE SETTINGS
# --------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("DB_USER", "user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
# --------------------------------------------------------------
# END DATABASE SETTINGS
# --------------------------------------------------------------


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



# --------------------------------------------------------------
# EMAIL SETTINGS
# --------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
if EMAIL_USE_TLS:
    EMAIL_USE_TLS = True
else:
    EMAIL_USE_TLS = False
EMAIL_HOST_USER = os.environ.get("DONOT_REPLY_EMAIL")
DISPLAY_NAME = "Udemy Course"
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
# --------------------------------------------------------------
# END EMAIL SETTINGS
# --------------------------------------------------------------


# --------------------------------------------------------------
# RECAPTCHA SETTINGS
# --------------------------------------------------------------
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
# --------------------------------------------------------------
# END RECAPTCHA SETTINGS
# --------------------------------------------------------------

# --------------------------------------------------------------
# COOKIE SETTINGS
# --------------------------------------------------------------
COOKIE_BOT = os.environ.get("COOKIE_BOT",None)
# --------------------------------------------------------------
# END COOKIE SETTINGS
# --------------------------------------------------------------
