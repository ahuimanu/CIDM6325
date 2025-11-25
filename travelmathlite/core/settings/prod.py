"""Production settings.

Import shared settings from base and enforce production-safe defaults.
This module intentionally raises if required secrets are missing to avoid
accidentally starting in an insecure state.
"""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403
from .base import env

# Enforce production defaults
DEBUG = False

# SECRET_KEY must be present in production
try:
    SECRET_KEY = env("SECRET_KEY")
except Exception as exc:  # environ will raise if missing
    raise ImproperlyConfigured("Missing required SECRET_KEY for production") from exc

# ALLOWED_HOSTS must be set for prod
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS must be set in production")

# Security hardening
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SECURE_HSTS_SECONDS = int(env("SECURE_HSTS_SECONDS", default="31536000"))
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# WhiteNoise and static serving are available when enabled in environment
USE_WHITENOISE = env.bool("USE_WHITENOISE", default=True)
