"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()
if os.getenv("USE_WHITENOISE", "0").lower() in ("1", "true", "yes"):
    try:
        from django.conf import settings
        from whitenoise import WhiteNoise

        static_root = getattr(settings, "STATIC_ROOT", None)
        if static_root:
            application = WhiteNoise(application, root=str(static_root))
    except Exception:
        # If WhiteNoise isn't available in the environment, fail gracefully.
        pass
