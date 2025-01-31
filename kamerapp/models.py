from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class Langue(models.Model):
    nomlangue = models.CharField(max_length=50, unique=True, default="vide")
    description = models.CharField(max_length=200, default="description")
    image = models.ImageField(upload_to='Image_langue/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, default="Ewondo")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nomlangue)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nomlangue

class Cours(models.Model):
    titre = models.CharField(max_length=100, default="vide")
    langue = models.ForeignKey(Langue, related_name='cours',on_delete=models.CASCADE, null=True)
    slug = models.SlugField(unique=True, blank=True, default="Ewondo")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titre} ({self.langue})"  # Retourne une chaîne formatée


class CustomUser(AbstractUser):
    tel = models.CharField(max_length=15, blank=True)
    langue = models.CharField(max_length=30, blank=True)
    langues = models.ManyToManyField(Langue, blank=True, related_name="utilisateurs")
    aire = models.CharField(max_length=50, blank=True, default="vide")
    is_teacher = models.BooleanField(default=False)
    image_user = models.ImageField(upload_to='profil/', default='profil/utilisateur.png',  # Chemin vers l'image par défaut
        null=True,blank=True,max_length=None)
    cours_suivis = models.ManyToManyField(Cours, blank=True, related_name="utilisateurs")
    sexe = models.CharField(max_length=10, choices=[
        ('male', 'Homme'),
        ('female', 'Femme'),
    ], blank=True)

    def __str__(self):
        return self.email
    

class Chapitre(models.Model):
    titre = models.CharField(max_length=100, default="vide")
    cours = models.ForeignKey(Cours, related_name='chapitres',on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.titre  # Retourne le titre du chapitre
    
class Exercice(models.Model):
    titre = models.CharField(max_length=100, default="vide")
    cours = models.ForeignKey(Cours, related_name='exercices',on_delete=models.CASCADE, null=True)
    contenu = models.TextField(default="vide")
    réponse = models.TextField(default="vide")

    def __str__(self):
        return self.titre  # Retourne le titre de l'exercice
    
class Leçon(models.Model):
    chap = models.ForeignKey(Chapitre, on_delete=models.CASCADE, related_name='lecons', null=True)
    titre = models.CharField(max_length=255, null=True)
    contenu = models.TextField()

    def __str__(self):
        return self.titre

class Progression(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    langue = models.ForeignKey(Langue, on_delete=models.CASCADE)
    niveau_actuel = models.CharField(max_length=20, default="vide")  # débutant, intermédiaire, avancé, etc.
    cours_suivis = models.ManyToManyField(Cours)

class Dictionnaire(models.Model):
    mot_francais = models.CharField(max_length=100, default=None)
    mot_traditionnel = models.CharField(max_length=100, default=None)  # Changé en CharField
    langue_traditionnelle = models.CharField(max_length=50, default=None)
    image = models.ImageField(upload_to='dico/', default='dico/question.gif',  # Chemin vers l'image par défaut
        null=True,blank=True,max_length=None)
    audio = models.FileField(upload_to='audios/', default='dico/question.gif', null=True)  # Chemin pour stocker les fichiers audio

    def __str__(self):
        return self.mot_francais    
    

class Ressource(models.Model):
    TYPRES = [
        ('DOC', 'Document'),
        ('VID', 'Vidéo'),
        ('AUD', 'Audio')
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    langue = models.CharField(max_length=50)
    type = models.CharField(max_length=3, choices=TYPRES)
    fichier = models.FileField(upload_to='ressources/')  # Chemin vers les fichiers
    username = models.ForeignKey(CustomUser, related_name="user", on_delete=models.CASCADE, null=True)  # Ajout du champ username

    def __str__(self):
        return self.titre

class Quiz(models.Model):
    title = models.CharField(max_length=100, null=True)
    partie = models.CharField(max_length=10, null=True)
    level = models.CharField(max_length=30, null=True)  # e.g., 'Débutant', 'Intermédiaire', 'Avancé'
    langue = models.ForeignKey(Langue, on_delete=models.CASCADE, null=True)  # Référence à la langue
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.langue)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=50, choices=[('MCQ', 'Choix Multiples'), ('TF', 'Vrai/Faux')])
    image_question = models.ImageField(upload_to='question/', default='question/question.gif',  # Chemin vers l'image par défaut
        null=True,blank=True,max_length=None)
    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserScore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    stars = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} : {self.score} points, {self.stars} étoiles"

class Expression(models.Model):
    expression = models.CharField(max_length=100)
    texte = models.CharField(max_length=100)
    langue = models.CharField(max_length=50, null=True)
    audio = models.FileField(upload_to='audios/')  # Chemin pour stocker les fichiers audio

    def __str__(self):
        return self.texte
     
class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    is_response = models.BooleanField(default=False)  # Indique si c'est une répon

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="comments")  # Lien avec la notification
    message = models.TextField()
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # L'utilisateur qui a posté le commentaire
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.username} on {self.notification.title}"
