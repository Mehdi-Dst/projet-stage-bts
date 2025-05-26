import django
import os
import joblib
from datetime import date
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Vue pour prédire si un employé va quitter l’entreprise
# Nombre de congés pris par l’employé
# Vérifie si l’employé est affecté à une équipe
# Ancienneté en jours

# Configuration de l'environnement Django pour accéder aux modèles
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

# Import des modèles Django nécessaires
from myapp.models import Employee, TeamMember, Leave

# Fonction pour construire le jeu de données à partir des données Django
def build_dataset():
    data = []
    # Parcourt tous les employés dans la base de données
    for emp in Employee.objects.all():
        # Compte le nombre de congés pris par l'employé
        leaves = Leave.objects.filter(employee=emp).count()
        # Récupère les liens entre l'employé et les équipes
        teams = TeamMember.objects.filter(employee=emp)
        # Vérifie si l'employé a quitté au moins une équipe
        left_team = any(tm.date_left is not None for tm in teams)
        # Calcule la durée d'ancienneté en jours depuis la date d'embauche
        tenure = (date.today() - emp.hire_date).days
        # Ajoute les informations dans une liste sous forme de dictionnaire
        data.append({
            "tenure_days": tenure,
            "num_leaves": leaves,
            "in_team": teams.exists(),
            "has_left_team": int(left_team)
        })
    # Retourne un DataFrame pandas construit à partir de la liste de dictionnaires
    return pd.DataFrame(data)

# Fonction pour entraîner le modèle de prédiction
def train_model():
    # Construction du dataset
    df = build_dataset()
    # Sélection des caractéristiques (features) pour l'entraînement
    X = df[["tenure_days", "num_leaves", "in_team"]]
    # Variable cible (label) à prédire
    y = df["has_left_team"]

    # Instanciation du modèle Random Forest
    model = RandomForestClassifier()
    # Entraînement du modèle sur les données
    model.fit(X, y)
    # Sauvegarde du modèle entraîné dans un fichier
    joblib.dump(model, "myapp/ml/attrition_model.joblib")
    print("✅ Attrition model trained and saved.")

# Point d'entrée du script
if __name__ == "__main__":
    train_model()
