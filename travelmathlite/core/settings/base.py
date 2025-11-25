"""Base settings for the project.

Contains environment-driven defaults and shared configuration.
Use `django-environ` to parse env vars and allow a `.env` file for local development.
"""

import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# `base.py` lives at `travelmathlite/core/settings/base.py`, so go three
# levels up to reach the project root `travelmathlite`.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)

# Read a .env file at project root if present (local convenience)
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(str(env_file))


# General
SECRET_KEY = env("SECRET_KEY", default="change-me-local-dev")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Domain apps
    "apps.calculators",
    "apps.airports",
    "apps.accounts",
    "apps.trips",
    "apps.search",
    "apps.base",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Request ID and timing middleware - must be early for logging
    "core.middleware.RequestIDMiddleware",
    # WhiteNoise placed here so deployments that enable it get static serving
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Cache headers middleware - must be after auth to check user state
    "core.middleware.CacheHeaderMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# Default to a local sqlite file when DATABASE_URL is not provided.
DATABASE_URL = env("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
DATABASES = {"default": env.db_url_config(DATABASE_URL)}


# Cache
# Use locmem for local development; support CACHE_URL for Redis/file-based in production.
# Default TTL is 300 seconds (5 minutes).
CACHES = {
    "default": {
        "BACKEND": env(
            "CACHE_BACKEND",
            default="django.core.cache.backends.locmem.LocMemCache",
        ),
        "LOCATION": env("CACHE_LOCATION", default="travelmathlite-cache"),
        "TIMEOUT": int(env("CACHE_TIMEOUT", default="300")),  # 5 minutes default
        "OPTIONS": {
            "MAX_ENTRIES": int(env("CACHE_MAX_ENTRIES", default="1000")),
        },
        "KEY_PREFIX": env("CACHE_KEY_PREFIX", default="travelmathlite"),
    }
}

# Alternative: use django-environ's cache_url for URL-based configuration
# Uncomment to use CACHE_URL environment variable parsing:
# CACHES = {"default": env.cache_url("CACHE_URL", default="locmem://")}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static and media
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = Path(os.getenv("STATIC_ROOT", BASE_DIR / "staticfiles"))
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", BASE_DIR / "media"))

# Manifest static policy fallback
USE_MANIFEST_STATIC = os.getenv("USE_MANIFEST_STATIC", "0").lower() in ("1", "true", "yes")


if not DEBUG or USE_MANIFEST_STATIC:
    STATICFILES_STORAGE = os.getenv(
        "STATICFILES_STORAGE",
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    )

WHITENOISE_MAX_AGE = int(os.getenv("WHITENOISE_MAX_AGE", "31536000"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth and app defaults
LOGIN_REDIRECT_URL = "base:index"
LOGOUT_REDIRECT_URL = "base:index"

# Calculator defaults (kept from previous settings)
ROUTE_FACTOR: float = float(os.getenv("ROUTE_FACTOR", "1.2"))
AVG_SPEED_KMH: float = float(os.getenv("AVG_SPEED_KMH", "80"))
FUEL_PRICE_PER_LITER: float = float(os.getenv("FUEL_PRICE_PER_LITER", "1.50"))
FUEL_ECONOMY_L_PER_100KM: float = float(os.getenv("FUEL_ECONOMY_L_PER_100KM", "7.5"))


# Logging configuration
# Structured JSON logging with request metadata per ADR-1.0.9
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "core.logging.JSONFormatter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
