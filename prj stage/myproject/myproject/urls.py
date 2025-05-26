from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

from myapp.admin import custom_admin_site
from myapp.views import chatbot_view, predict_attrition, predict_project_duration

urlpatterns = [
    # Redirige la racine '/' vers la page d'administration
    path('', lambda request: redirect('admin/', permanent=False)),
    
    # Page d'administration personnalisée
    path('admin/', custom_admin_site.urls),
    
    # URL pour interagir avec le chatbot
    path('chatbot/ask/', chatbot_view, name='chatbot_ask'),  # ✅ Ajouté
    
    # URL pour la prédiction du taux de rotation (attrition)
    path('predict/attrition/', predict_attrition, name='predict_attrition'),
    
    # URL pour la prédiction de la durée des projets
    path('predict/duration/', predict_project_duration, name='predict_project_duration'),
]
