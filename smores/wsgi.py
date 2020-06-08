"""
WSGI config for smores project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from werkzeug.wsgi import DispatcherMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smores.settings")

application = get_wsgi_application()

from .frontend import app as frontend

application = DispatcherMiddleware(frontend, {
    '/admin': application,
    '/dj-static': application,
})
