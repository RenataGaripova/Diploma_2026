# Python modules
from pathlib import Path

# Project modules
from settings.conf import *  # noqa: F403

# ----------------------------------------------
# Path
#
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = "settings.urls"
WSGI_APPLICATION = "settings.wsgi.application"
ASGI_APPLICATION = "settings.asgi.application"

# ----------------------------------------------
# Apps
#
DJANGO_AND_THIRD_PARTY_APPS = [
    "modeltranslation",  # must be before django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
]
PROJECT_APPS = [
    "apps.abstracts.apps.AbstractsConfig",
    "apps.companies.apps.CompaniesConfig",
    "apps.users.apps.UsersConfig",
]
INSTALLED_APPS = DJANGO_AND_THIRD_PARTY_APPS + PROJECT_APPS
AUTH_USER_MODEL = "users.CustomUser"

# ----------------------------------------------
# Middleware | Templates | Validators | Cache
#
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ----------------------------------------------
# Internationalization
#
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
ENGLISH_LANGUAGE_CODE = "en"
ENGLISH_LANGUAGE_LABEL = "English"
RUSSIAN_LANGUAGE_CODE = "ru"
RUSSIAN_LANGUAGE_LABEL = "Russian"
KAZAKH_LANGUAGE_CODE = "kk"
KAZAKH_LANGUAGE_LABEL = "Kazakh"
LANGUAGES = (
    (ENGLISH_LANGUAGE_CODE, ENGLISH_LANGUAGE_LABEL),
    (RUSSIAN_LANGUAGE_CODE, RUSSIAN_LANGUAGE_LABEL),
    (KAZAKH_LANGUAGE_CODE, KAZAKH_LANGUAGE_LABEL),
)
LOCALE_PATHS = [
    BASE_DIR / "locale",
]
MODELTRANSLATION_DEFAULT_LANGUAGE = ENGLISH_LANGUAGE_CODE
MODELTRANSLATION_LANGUAGES = (
    ENGLISH_LANGUAGE_CODE,
    RUSSIAN_LANGUAGE_CODE,
    KAZAKH_LANGUAGE_CODE,
)
MODELTRANSLATION_FALLBACK_LANGUAGES = (ENGLISH_LANGUAGE_CODE,)

# ----------------------------------------------
# Static | Media
#
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
SCREENSHOTS_URL = "/screenshots/"
SCREENSHOTS_ROOT = BASE_DIR / "screenshots"
ATTACHMENTS_URL = "/attachments/"
ATTACHMENTS_ROOT = BASE_DIR / "attachments"
OWNER_REGISTRATION_URL = "new_owner"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
