"""
Django settings for _core project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

import logfire
from pydantic import SecretStr

from .github_creds import facebook_key, facebook_secret, github_key, github_secret

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-bg45soje9%01^7d08n918u)-mnn5&(tv(+3wa67k)wvqr(7!_1"  # noqa: S105

ASGI_APPLICATION = "_core.asgi.application"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # UNFOLD ADMIN CHANGES
    # "unfold",  # before django.contrib.admin
    # "unfold.contrib.filters",  # optional, if special filters are needed
    # "unfold.contrib.forms",  # optional, if special form elements are needed
    # "unfold.contrib.inlines",  # optional, if special inlines are needed
    # "unfold.contrib.import_export",  # optional, if django-import-export package is used
    # "unfold.contrib.guardian",  # optional, if django-guardian package is used
    # "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    # UNOFFICIAL THIRD PARTY
    "django_tasks",
    "django_tasks.backends.database",
    "social_django",
    "django_htmx",
    "ninja",
    'waffle',
    # OFFICIAL THIRD PARTY
    "daphne",
    # BUILT-IN
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # local apps
    "app_soiled.apps.AppSoiledConfig",
    "app_traps.apps.AppTrapsConfig",
    # backends
    "backend_feature_flags.apps.BackendFeatureFlagsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    'waffle.middleware.WaffleMiddleware',
]

ROOT_URLCONF = "_core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "_core" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "_core.wsgi.application"

# from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _

# UNFOLD = {
#     "SITE_HEADER": _("Turbo Admin"),
#     "SITE_TITLE": _("Turbo Admin"),
#     "SIDEBAR": {
#         "show_search": True,
#         "show_all_applications": True,
#         "navigation": [
#             {
#                 "title": _("Navigation"),
#                 "separator": False,
#                 "items": [
#                     {
#                         "title": _("Users"),
#                         "icon": "person",
#                         "link": reverse_lazy("admin:backend_user_changelist"),
#                     },
#                     {
#                         "title": _("Groups"),
#                         "icon": "label",
#                         "link": reverse_lazy("admin:auth_group_changelist"),
#                     },
#                 ],
#             },
#         ],
#     },
# }

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "transaction_mode": "EXCLUSIVE",
            "timeout": 5,  # seconds
            "init_command": """
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA mmap_size = 134217728;
                PRAGMA journal_size_limit = 27103364;
                PRAGMA cache_size=2000;
            """,
        },
    }
}

NINJA_PAGINATION_PER_PAGE = 500

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",
]

SOCIAL_AUTH_GITHUB_KEY = github_key
SOCIAL_AUTH_GITHUB_SECRET = github_secret

SOCIAL_AUTH_FACEBOOK_KEY = facebook_key
SOCIAL_AUTH_FACEBOOK_SECRET = facebook_secret
SOCIAL_AUTH_FACEBOOK_APP_NAMESPACE = ""

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Chicago"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = (
    BASE_DIR / "_core" / "static",
    BASE_DIR / "_core" / "static" / "img",
    BASE_DIR / "_core" / "static" / "css",
    BASE_DIR / "_core" / "static" / "js",
)
STATIC_ROOT = BASE_DIR / "assets"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CACHES = {
    "default": {
        "BACKEND": "diskcache.DjangoCache",
        "LOCATION": BASE_DIR / "_core" / "local-storage" / "cache",
        "TIMEOUT": 1800,
        # ^-- Django setting for default timeout of each key.
        "SHARDS": 8,
        "DATABASE_TIMEOUT": 0.010,  # 10 milliseconds
        # ^-- Timeout for each DjangoCache database transaction.
        "OPTIONS": {
            "size_limit": 2**30  # 1 gigabyte
        },
    },
}


TASKS = {
    "default": {
        "BACKEND": "django_tasks.backends.database.DatabaseBackend",
        "QUEUES": ["default"],
    }
}


# Add the following lines at the end of the file
logfire.configure()
logfire.instrument_django()
# logfire.instrument_pydantic()

ONEPASS_TOKEN = SecretStr(secret_value=os.getenv("OP_SERVICE_ACCOUNT_TOKEN"))
