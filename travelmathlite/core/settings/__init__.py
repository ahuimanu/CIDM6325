"""Settings package for the Django project.

Default import path `core.settings` will load local development settings.
To use production settings, set `DJANGO_SETTINGS_MODULE=core.settings.prod`.

This module intentionally re-exports the chosen settings module so existing
invocations that default to `core.settings` (e.g., `manage.py`) continue to work.
"""

from .local import *  # noqa: F401,F403
