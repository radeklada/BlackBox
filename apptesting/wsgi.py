"""
WSGI config for apptesting project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
        sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apptesting.settings')

application = get_wsgi_application()
