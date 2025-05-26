# 📦 Importation des modules nécessaires de Django
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count

# 📦 Importation des modèles créés dans le projet
from .models import Department, Employee, Leave, Role, Team, TeamMember, Project
from django.contrib.auth.models import User, Group

# ✅ Création d'une classe personnalisée pour l'interface d'administration
class CustomAdminSite(admin.AdminSite):
    # 🏷️ En-têtes personnalisés pour l'interface d'administration
    site_header = "My Admin Dashboard"
    site_title = "Admin Panel"
    index_title = "Welcome to the Dashboard"

    # 🔁 Redéfinition de la méthode get_urls pour ajouter une page d'accueil personnalisée
    def get_urls(self):
        urls = super().get_urls()  # Récupère les URLs par défaut
        custom_urls = [
            # 🏠 Ajoute une URL personnalisée pour afficher le tableau de bord
            path('', self.admin_view(self.dashboard), name='dashboard'),
        ]
        return custom_urls + urls  # Combine les URLs personnalisées avec les URLs par défaut

    # 📊 Méthode pour générer la page de tableau de bord personnalisée
    def dashboard(self, request):
        # 👥 Préparation des données pour un graphique : nombre d'employés par département
        department_data = Department.objects.annotate(emp_count=Count('employee'))
        dept_names = [dept.department_name for dept in department_data]  # Noms des départements
        dept_counts = [dept.emp_count for dept in department_data]        # Nombre d'employés par département

        # 📦 Contexte à envoyer au template HTML
        context = dict(
            self.each_context(request),  # Contexte par défaut de Django
            departments=Department.objects.count(),
            employees=Employee.objects.count(),
            leaves=Leave.objects.count(),
            roles=Role.objects.count(),
            teams=Team.objects.count(),
            members=TeamMember.objects.count(),
            projects=Project.objects.count(),
            department_names=dept_names,
            department_counts=dept_counts,
        )
        # 📄 Retourne le template avec les données contextuelles
        return TemplateResponse(request, "admin/custom_dashboard.html", context)

# ✅ Instanciation du site d'administration personnalisé
custom_admin_site = CustomAdminSite(name='custom_admin')

# ✅ Enregistrement de tous les modèles pour qu'ils apparaissent dans l'interface d'administration
custom_admin_site.register(Department)
custom_admin_site.register(Employee)
custom_admin_site.register(Leave)
custom_admin_site.register(Role)
custom_admin_site.register(Team)
custom_admin_site.register(TeamMember)
custom_admin_site.register(Project)
custom_admin_site.register(User)   # Utilisateurs du système
custom_admin_site.register(Group)  # Groupes d'utilisateurs
