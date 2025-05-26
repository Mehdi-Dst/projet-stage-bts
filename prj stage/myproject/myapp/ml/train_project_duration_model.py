import django  # Import de Django pour utiliser ses fonctionnalités dans un script externe
import os  # Pour manipuler les variables d'environnement
import joblib  # Pour sauvegarder et charger des modèles ML
import pandas as pd  # Pour manipuler des données sous forme de DataFrame
from datetime import date  # Pour gérer les dates
from sklearn.linear_model import LinearRegression  # Modèle de régression linéaire de sklearn
from sklearn.model_selection import train_test_split  # Fonction pour séparer les données en train/test (non utilisée ici)

#pour estimer la durée d’un projet déjà terminé
# Taille de l’équipe du projet
# Chef de l’équipe
# Ancienneté du leader en jours

# Définition de la variable d'environnement pour configurer Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()  # Initialisation de Django pour pouvoir utiliser ses modèles

# Import des modèles Django nécessaires à l'analyse
from myapp.models import Project, TeamMember, Employee

# Fonction qui construit un DataFrame à partir des données du modèle Project
def build_dataset():
    rows = []
    # Parcourt tous les projets qui ont une date de fin (finie)
    for p in Project.objects.exclude(end_date=None):
        # Compte le nombre de membres dans l'équipe associée au projet
        team_size = TeamMember.objects.filter(team=p.team).count()
        # Récupère le responsable (lead) de l'équipe
        lead = p.team.team_lead
        # Calcule l'ancienneté du responsable en jours, ou 0 s'il n'y a pas de lead
        lead_tenure = (date.today() - lead.hire_date).days if lead else 0
        # Calcule la durée du projet en jours
        duration = (p.end_date - p.start_date).days
        # Ajoute un dictionnaire avec les informations extraites dans la liste rows
        rows.append({
            "team_size": team_size,
            "lead_tenure": lead_tenure,
            "duration_days": duration
        })
    # Convertit la liste en DataFrame pandas pour analyse
    return pd.DataFrame(rows)

# Fonction qui entraîne un modèle de régression pour prédire la durée du projet
def train_model():
    df = build_dataset()  # Création du dataset
    X = df[["team_size", "lead_tenure"]]  # Variables explicatives
    y = df["duration_days"]  # Variable cible

    model = LinearRegression()  # Initialisation du modèle de régression linéaire
    model.fit(X, y)  # Entraînement du modèle sur les données
    joblib.dump(model, "myapp/ml/duration_model.joblib")  # Sauvegarde du modèle entraîné
    print("✅ Project duration model trained and saved.")  # Message de confirmation

# Exécution du script uniquement si c'est le fichier principal exécuté
if __name__ == "__main__":
    train_model()
