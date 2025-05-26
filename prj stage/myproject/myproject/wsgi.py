"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Définit la variable d'environnement pour les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Crée l'application WSGI qui sert à déployer Django sur un serveur compatible WSGI
application = get_wsgi_application()
