python manage.py runserver


del db.sqlite3


python manage.py makemigrations
python manage.py migrate

python manage.py makemigrations admin_interface
python manage.py migrate


python manage.py migrate --run-syncdb

Vérification dans la base de données :
sqlite3 db.sqlite3
.tables      # Liste toutes les tables dans la base de données



rm db.sqlite3
python manage.py makemigrations admin_interface
python manage.py migrate


python manage.py createsuperuser
testadmin@gmail.com
test2025



python manage.py shell
from django.contrib.auth.models import User
admins = User.objects.filter(is_superuser=True)
for admin in admins:
    print(f"ID: {admin.id}, Username: {admin.username}, Email: {admin.email}")



    my_project/
│── my_app/
│   ├── models/       # Modèles (base de données)
│   ├── views/        # Vue logique (contrôleurs)
│   ├── serializers/  # Sérialisation des données (si API)
│   ├── services/     # Logique métier
│   ├── repositories/ # Accès aux données
│   ├── urls.py       # Routes
│   ├── tests/        # Tests unitaires
│   ├── admin.py      # Configuration admin Django
│   ├── apps.py       # Configuration de l'application
│── config/
│   ├── settings/     # Fichiers de configuration séparés
│── manage.py


