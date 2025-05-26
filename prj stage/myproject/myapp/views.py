# Importation des modules nécessaires pour les vues Django
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot import ask_openai  # Fonction de génération de réponse depuis OpenAI

# Vue de la page d’accueil, renvoie un message texte simple
def home(request):
    return HttpResponse("Welcome to your internship project!")

# Vue du chatbot, accepte uniquement les requêtes POST avec une question
@csrf_exempt  # Désactive la protection CSRF pour permettre les tests externes (ex: Postman)
def chatbot_view(request):
    if request.method == "POST":
        question = request.POST.get("question", "")  # Récupère la question envoyée
        if not question:
            return JsonResponse({"answer": "Please enter a question."})  # Si pas de question, message d’erreur
        answer = ask_openai(question)  # Génère une réponse via OpenAI
        return JsonResponse({"answer": answer})  # Renvoie la réponse sous forme JSON
    return JsonResponse({"error": "Only POST requests allowed."})  # Refuse les requêtes GET, etc.

# Importations supplémentaires pour les prédictions ML
import os
import joblib  # Utilisé pour charger les modèles ML
from datetime import date
from django.http import JsonResponse  # (Déjà importé plus haut, redondant mais pas grave)
from myapp.models import Employee, TeamMember, Project  # Importation des modèles Django

# Chargement des modèles de Machine Learning une seule fois au démarrage
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Récupère le répertoire du fichier actuel
ATTRITION_MODEL = joblib.load(os.path.join(BASE_DIR, "ml/attrition_model.joblib"))  # Modèle pour prédiction départ employés
DURATION_MODEL = joblib.load(os.path.join(BASE_DIR, "ml/duration_model.joblib"))  # Modèle pour estimation durée projets

# Importations répétées (déjà faites en haut, mais gardées ici selon ta structure)
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot import ask_openai

# Vue d’accueil (déjà définie plus haut, redondante)
def home(request):
    return HttpResponse("Welcome to your project!")

# Vue chatbot (déjà définie plus haut, redondante)
@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        question = request.POST.get("question", "")
        if not question:
            return JsonResponse({"answer": "Please enter a question."})
        answer = ask_openai(question)
        return JsonResponse({"answer": answer})
    return JsonResponse({"error": "Only POST requests allowed."})

# Vue pour prédire si un employé va quitter l’entreprise
def predict_attrition(request):
    emp = Employee.objects.first()  # Récupère un employé (le premier de la BDD)
    if not emp:
        return JsonResponse({"error": "No employee found"}, status=404)  # Aucun employé trouvé

    leaves = emp.leave_set.count()  # Nombre de congés pris par l’employé
    in_team = TeamMember.objects.filter(employee=emp).exists()  # Vérifie si l’employé est affecté à une équipe
    tenure = (date.today() - emp.hire_date).days  # Ancienneté en jours

    prediction = ATTRITION_MODEL.predict([[tenure, leaves, int(in_team)]])[0]  # Prédiction du modèle
    result = "Will Leave" if prediction else "Stays"  # Conversion du résultat en texte

    return JsonResponse({"employee": str(emp), "prediction": result})  # Retourne la prédiction

# Vue pour estimer la durée d’un projet déjà terminé
def predict_project_duration(request):
    project = Project.objects.exclude(end_date=None).first()   # Récupère un projet complété
    if not project:
        return JsonResponse({"error": "No completed project found"}, status=404)  # Aucun projet terminé trouvé

    team_size = TeamMember.objects.filter(team=project.team).count()  # Taille de l’équipe du projet
    lead = project.team.team_lead  # Chef de l’équipe
    lead_tenure = (date.today() - lead.hire_date).days if lead else 0  # Ancienneté du leader en jours

    prediction = DURATION_MODEL.predict([[team_size, lead_tenure]])[0]  # Prédiction du modèle

    return JsonResponse({
        "project": str(project),
        "estimated_duration_days": int(prediction)  # Résultat de la prédiction arrondi en nombre entier
    })
