#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main():
    """Run administrative tasks."""
    # Définit la variable d'environnement pour les paramètres Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        # Importe la fonction pour exécuter les commandes Django en ligne de commande
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Affiche un message d'erreur clair si Django n'est pas installé ou non trouvé
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Exécute la commande passée en argument dans la ligne de commande
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Point d'entrée du script : lance la fonction main()
    main()
