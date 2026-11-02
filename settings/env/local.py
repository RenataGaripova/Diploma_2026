# Python modules

# Project modules
from settings.base import *  # noqa: F403

# Configure local settings
DEBUG = True
INTERNAL_IPS = [
    "127.0.0.1",
]
ALLOWED_HOSTS = ["*"]

# ----------------------------------------------
# Database configuration
#
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}
