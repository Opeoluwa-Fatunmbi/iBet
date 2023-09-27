"""
ASGI config for iBet project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from decouple import config

SETTINGS = config("SETTINGS")


from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"iBet.settings.{SETTINGS}",
)

application = get_asgi_application()
