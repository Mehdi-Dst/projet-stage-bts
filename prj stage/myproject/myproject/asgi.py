"""
ASGI config for myproject project.

Il expose la callable ASGI au niveau du module sous le nom `application`.

Pour plus d'informations, voir la documentation officielle :
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os  # Pour gérer les variables d'environnement

from django.core.asgi import get_asgi_application  # Import de la fonction qui retourne l'application ASGI

# Définit la variable d'environnement indiquant où se trouve la configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Récupère l'application ASGI Django, utilisée pour déployer le projet avec des serveurs ASGI
application = get_asgi_application()
