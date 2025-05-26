from django.apps import AppConfig  # 📦 Importe la classe de configuration de l'application Django

# ✅ Configuration de l'application "myapp"
class MyappConfig(AppConfig):
    # 🧠 Définit le type de champ automatique par défaut pour les clés primaires
    default_auto_field = 'django.db.models.BigAutoField'
    
    # 🏷️ Nom de l'application (doit correspondre au nom du dossier de l'application)
    name = 'myapp'
