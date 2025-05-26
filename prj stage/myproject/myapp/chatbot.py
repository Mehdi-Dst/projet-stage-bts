import openai  # 📦 Importe la bibliothèque OpenAI pour utiliser l'API ChatGPT
from .models import Employee, Department, Leave  # 📦 Importe les modèles nécessaires depuis l'app Django

# ⚠️ Clé API OpenAI en dur (non recommandé pour la production)
openai.api_key = ""
# ✅ Fonction qui récupère les données depuis la base de données
def get_context_from_db():
    # 🔢 Nombre total d'employés
    emp_count = Employee.objects.count()

    # 📋 Liste des noms de départements
    dept_list = Department.objects.values_list('department_name', flat=True)

    # 🔢 Nombre total de demandes de congés
    leave_count = Leave.objects.count()

    # 🧾 Retourne un texte formaté avec les informations
    return f"""
    Total Employees: {emp_count}
    Departments: {', '.join(dept_list)}
    Leaves Requested: {leave_count}
    """

# ✅ Fonction pour interroger l'API d'OpenAI avec un contexte
def ask_openai(question):
    # 📊 Récupère les données de contexte depuis la base
    context = get_context_from_db()

    # 🧠 Crée un prompt combinant le contexte et la question
    prompt = f"""
You are an assistant for a company admin dashboard. Here's current data:

{context}

Answer this question: {question}
"""

    try:
        # 📡 Appelle l'API ChatGPT avec le modèle GPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        # ✅ Retourne la réponse générée par l'IA
        return response.choices[0].message.content.strip()
    except Exception as e:
        # ⚠️ Gestion des erreurs en cas d'échec de l'appel API
        return f"⚠️ Error: {str(e)}"
    



