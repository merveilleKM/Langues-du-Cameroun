Etapes pour ouvrir le projet

1- se place dans un dossier vide, creer l'environnement virtuel avec la requete : python -m venv env (ici mon environnement virtuel s'appelle env)
2- activer l'environnement env\Scripts\activate
3- install django avec pip install django
4- se positionner dans la meme racine que l'environnement virtuel
5- creer le projet : django-admin startproject monprojet, ici c'est kamer
6- creer l'application avec python manage.py startapp nomdelapplication, ici c'est kamerapp
7- installer les packages necessaires : pip install mysqlclient, pip install pillow 
8- configurer la base de donnees dans settings.py du projet, ici c'est kamerapp
9- faire les migrations : python manage.py makemigrations ensuite python manage.py migrate
10- Ouvrir l'application dans ton navigateur a l'adresse : 127.0.0.0:8080