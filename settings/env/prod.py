# Python modules
from decouple import Csv, config

# Project modules
from settings.base import *  # noqa: F403


# Configure local variables
DEBUG = False
ALLOWED_HOSTS = config("SMARTSTOCK_ALLOWED_HOSTS", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("SMARTSTOCK_CSRF_TRUSTED_ORIGINS", cast=Csv())

# ----------------------------------------------
# Security
#
# Django runs behind a reverse proxy (nginx) that terminates HTTPS
# and sets the X-Forwarded-Proto header.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = config("SMARTSTOCK_SECURE_SSL_REDIRECT", default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
# Browsers remember HSTS, so enable it only once HTTPS works reliably.
SECURE_HSTS_SECONDS = config("SMARTSTOCK_SECURE_HSTS_SECONDS", default=0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# ----------------------------------------------
# Database configuration
#
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("SMARTSTOCK_DB_NAME", cast=str),
        "USER": config("SMARTSTOCK_DB_USER", cast=str),
        "PASSWORD": config("SMARTSTOCK_DB_PASSWORD", cast=str),
        "HOST": config("SMARTSTOCK_DB_HOST", cast=str),
        "PORT": config("SMARTSTOCK_DB_PORT", cast=str),
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,
    }
}
