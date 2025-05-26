# projet-stage-bts
projet de stage de 2 annee bts dia 

cd myproject   
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver --noreload

il vout faut acheter un api chatgpt open ai 


projet réalisé avec Django. Ce projet est une application web qui gère plusieurs aspects importants d’une entreprise, comme les employés, les équipes, les projets, et les congés.

J’ai construit une base de données MySQL pour stocker toutes ces informations et j’ai créé des modèles Django pour représenter les différentes entités comme les employés, les équipes et les projets.

Dans l’application, il y a un espace d’administration personnalisé où on peut ajouter, modifier ou supprimer des données. J’ai aussi développé des fonctionnalités spécifiques, comme un chatbot pour répondre à des questions, ainsi que deux modèles d’intelligence artificielle :

un modèle qui prédit le risque de départ des employés,

un autre qui estime la durée probable d’un projet selon la taille de l’équipe et l’expérience du chef de projet.

Pour cela,  bibliothèques scikit-learn pour entraîner ces modèles et joblib pour les sauvegarder et les réutiliser dans l’application.
