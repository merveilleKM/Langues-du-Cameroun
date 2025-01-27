from django.shortcuts import render, redirect
from .models import CustomUser, Cours, Langue, Quiz, Question, Dictionnaire, Notification, Ressource, Comment
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import UserUpdateForm, ProfileUpdateForm

def signin(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email_or_username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect('cours')  # Redirection sécurisée
        else:
            messages.error(request, "Identifiants invalides.")
    return render(request, 'signin.html')

def signup (request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        password = request.POST.get('password')
        langue = request.POST.get('langue')

        # Vérification si l'utilisateur existe déjà
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, 'signup.html')

        # Création de l'utilisateur
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            tel=tel,
            langue=langue,
            password=password
        )
        user.save()

        # Connexion automatique de l'utilisateur après inscription
        login(request, user)
        messages.success(request, "Inscription réussie. Bienvenue !")

    return render(request, 'signup.html')

def deconnect (request):
    logout(request)
    return render(request, 'deconnect.html')

def accueil (request):
    return render(request, 'index.html')

def dashboard (request):
    return render(request, 'plate/dash.html')

def cours (request):
    # Récupérer la langue de l'utilisateur
    user_langue = request.user.langue  # Assurez-vous que c'est bien le bon attribut
    
    # Filtrer les cours par langue
    cours = Langue.objects.filter(nomlangue=user_langue)  # Filtrer les cours selon la langue de l'utilisateur

    return render(request, 'plate/cours.html', {'cours': cours})

def detail(request, slug):
    # Récupérer la langue de l'utilisateur
    user_langue = request.user.langue  # Assurez-vous que c'est bien le bon attribut

    cours = get_object_or_404(Cours, slug=slug)
    dets = Cours.objects.filter(langue__nomlangue=user_langue)
    return render(request, 'plate/cours/detail.html', {'cours': cours, 'dets': dets})

def dico (request):
     
    return render(request, 'plate/cours/dico.html', {'dico': dico})

def quiz (request):

    return render(request, 'plate/cours/quiz.html', {'quiz': quiz})


def communaute(request):
    notifications = Notification.objects.filter(is_response=False)
     # Récupérer toutes les ressources (documents, vidéos, audio)
    ressources = Ressource.objects.all()

    return render(request, 'plate/communaute.html', {'notifications': notifications, 'ressources':ressources})

@login_required  # S'assurer que l'utilisateur est connecté
def publier(request):
   if request.method == "POST" and 'title' in request.POST and 'file' in request.FILES:
        # Créer une nouvelle ressource (document)
        document = Ressource(
            titre=request.POST['title'],
            description=request.POST.get['description'], 
            langue=request.POST.get('langue', ''),  # Langue optionnelle
            type='DOC',  # Assigner le type comme 'Document'
            fichier=request.FILES['file'],  # Le fichier téléchargé
            username=request.user  # L'utilisateur connecté est celui qui a posté le document
        )
        document.save()  # Enregistrer le document
        return redirect('communaute')  # Rediriger vers la page de la communauté après la publication

def commentaire(request):
    if request.method == "POST":
        if 'title' in request.POST and 'message' in request.POST:
            # Ajouter une nouvelle notification
            Notification.objects.create(
                title=request.POST['title'],
                message=request.POST['message'],
                username=request.user,  # Associer l'utilisateur connecté à la notification
                is_response=False  # Vous pouvez marquer ceci comme 'False' si c'est une question initiale
            )
            return redirect('communaute')  # Rediriger vers la page de la communauté après soumission

    return render(request, 'plate/community/commentaire.html')

def add_comment(request, notification_id):
    if request.method == "POST" and 'message' in request.POST:
        notification = get_object_or_404(Notification, id=notification_id)
        Comment.objects.create(
            notification=notification,
            message=request.POST['message'],
            username=request.user  # Utilisateur connecté
        )
        return redirect('communaute')  # Retour à la page communauté après l'ajout

    return redirect('communaute')  # En cas de requête GET, redirige simplement

def search(request):
    query = request.GET.get('q', '').strip()  # Récupère le terme de recherche
    notifications = Notification.objects.filter(
        Q(title__icontains=query) | Q(message__icontains=query)
    )
    ressources = Ressource.objects.filter(
        Q(langue__icontains=query) | Q(description__icontains=query)
    )
    comments = Comment.objects.filter(
        Q(message__icontains=query)
    )

    context = {
        'query': query,
        'notifications': notifications,
        'ressources': ressources,
        'comments': comments,
    }
    return render(request, 'plate/communaute.html', context)

def profil (request):
    user = request.user
    langues_disponibles = Langue.objects.all()  # Récupère toutes les langues disponibles

    if request.method == "POST":
        langue_id = request.POST.get('langue')  # Récupère l'ID de la langue sélectionnée
        if langue_id:
            try:
                nouvelle_langue = Langue.objects.get(id=langue_id)
                user.langues = nouvelle_langue  # Met à jour la langue d'apprentissage de l'utilisateur
                user.langue = nouvelle_langue.nomlangue  # Met à jour le champ "langue" pour plus de lisibilité (optionnel)
                user.save()  # Enregistre les modifications
                return redirect('profil')  # Recharge la page pour refléter les changements
            except Langue.DoesNotExist:
                pass  # Gestion des erreurs si la langue n'existe pas

    return render(request, 'plate/profile.html', {
        'user': user,
        'langues_disponibles': langues_disponibles,
    })

@login_required
def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('profil')
        else:
            messages.error(request, "Erreur lors de la mise à jour de votre profil.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user)

    return render(request, 'plate/profile_update.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
