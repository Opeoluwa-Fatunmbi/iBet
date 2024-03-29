"""
WSGI config for iBet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from decouple import config

SETTINGS = config("SETTINGS")


from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"iBet.settings.{SETTINGS}",
)

application = get_wsgi_application()

app = application
