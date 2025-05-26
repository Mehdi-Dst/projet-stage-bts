from django.db import models  # 📦 Importe les outils de création de modèles de Django

# ✅ Modèle pour les départements
class Department(models.Model):
    department_id = models.AutoField(primary_key=True)  # 🆔 ID unique auto-incrémenté
    department_name = models.CharField(max_length=50)  # 🏷️ Nom du département
    manager_id = models.IntegerField(null=True, blank=True)  # 🧑‍💼 ID du manager (optionnel)

    def __str__(self):
        return self.department_name  # 🔁 Affiche le nom du département dans l’interface admin

# ✅ Modèle pour les employés
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)  # 🆔 ID unique auto-incrémenté
    first_name = models.CharField(max_length=50)  # 👤 Prénom
    last_name = models.CharField(max_length=50)  # 👤 Nom
    email = models.EmailField(max_length=100, null=True, blank=True)  # 📧 Email (optionnel)
    phone_number = models.CharField(max_length=20, null=True, blank=True)  # 📱 Téléphone (optionnel)
    hire_date = models.DateField()  # 📅 Date d'embauche
    position = models.CharField(max_length=50, null=True, blank=True)  # 🧾 Poste (optionnel)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, db_column='department_id')  # 🔗 Lien vers le département

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # 🔁 Affichage dans l'admin

# ✅ Modèle pour les congés
class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)  # 🆔 ID unique auto-incrémenté
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')  # 🔗 Employé concerné
    leave_type_name = models.CharField(max_length=50)  # 🏷️ Type de congé (ex : maladie, vacances)
    start_date = models.DateField()  # 📅 Date de début
    end_date = models.DateField()  # 📅 Date de fin
    status = models.CharField(max_length=20)  # 📌 Statut (approuvé, en attente...)

    def __str__(self):
        return f"{self.leave_type_name} ({self.status})"  # 🔁 Affichage dans l'admin

# ✅ Modèle pour les rôles (membre, admin, dev, etc.)
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)  # 🆔 ID unique
    role_name = models.CharField(max_length=50)  # 🏷️ Nom du rôle
    description = models.TextField(null=True, blank=True)  # 📝 Description optionnelle

    def __str__(self):
        return self.role_name  # 🔁 Affichage dans l'admin

# ✅ Modèle pour les équipes
class Team(models.Model):
    team_id = models.AutoField(primary_key=True)  # 🆔 ID unique
    team_name = models.CharField(max_length=50)  # 🏷️ Nom de l’équipe
    team_lead = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="lead_of_team", db_column='team_lead_id')  # 🧑‍💼 Chef d’équipe (employé)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, db_column='department_id')  # 🔗 Département lié

    def __str__(self):
        return self.team_name  # 🔁 Affichage dans l'admin

# ✅ Modèle pour les membres d'équipe
class TeamMember(models.Model):
    team_member_id = models.AutoField(primary_key=True)  # 🆔 ID unique
    team = models.ForeignKey(Team, on_delete=models.CASCADE, db_column='team_id')  # 🔗 Équipe liée
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')  # 🔗 Employé lié
    date_joined = models.DateField(null=True, blank=True)  # 📅 Date d'entrée dans l'équipe
    date_left = models.DateField(null=True, blank=True)  # 📅 Date de sortie (si applicable)

    def __str__(self):
        return f"{self.employee} in {self.team}"  # 🔁 Affichage dans l'admin

# ✅ Modèle pour les projets
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)  # 🆔 ID unique
    project_name = models.CharField(max_length=100)  # 🏷️ Nom du projet
    start_date = models.DateField()  # 📅 Date de début
    end_date = models.DateField(null=True, blank=True)  # 📅 Date de fin (optionnelle)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, db_column='team_id')  # 🔗 Équipe responsable

    def __str__(self):
        return self.project_name  # 🔁 Affichage dans l'admin
