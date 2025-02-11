from django.shortcuts import render, redirect
from .models import CustomUser, Cours, Langue, Quiz, Question, Dictionnaire, Notification, Ressource, Comment, UserScore, Answer, Leçon, Vocabulaire, Dialogue, LigneDialogue, Exercice, Jeu
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import UserUpdateForm, ProfileUpdateForm
from django.http import JsonResponse
import json  
from django.utils.text import slugify

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
        if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Cet email ou nom d'utilisateur est déjà utilisé.")
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

@login_required
def dashboard(request):
    user_langue = request.user.langue  # Assurez-vous que c'est bien le bon attribut
    user_langues = Langue.objects.filter(nomlangue=user_langue)
    return render(request, 'plate/dash.html', {'cours': user_langues})
def cours(request):

    # Obtenez la langue par défaut de l'utilisateur (celle de l'inscription)
    langue_par_defaut = None
    if request.user.langue:  # Vérifie si une langue par défaut est définie
        try:
            langue_par_defaut = Langue.objects.get(nomlangue=request.user.langue)
        except Langue.DoesNotExist:
            pass

    # Récupérez toutes les langues liées à l'utilisateur
    autres_langues = request.user.langues.all()

    # Si la langue par défaut n'est pas déjà dans les langues associées, ajoutez-la temporairement
    if langue_par_defaut and langue_par_defaut not in autres_langues:
        autres_langues = [langue_par_defaut] + list(autres_langues)

    return render(request, 'plate/cours.html', {'cours': autres_langues})

def searchcours(request):
    user_langue = request.user.langue if request.user.langue else None
    query = request.GET.get('q', user_langue).strip()

    # Filtre les cours suivis par l'utilisateur OU les cours de la langue de l'utilisateur
    cours = Langue.objects.filter(
        Q(utilisateurs=request.user) | Q(nomlangue=user_langue)
    ).distinct()

    # Applique la recherche sur les cours filtrés
    if query:
        cours = cours.filter(
            Q(description__icontains=query) | Q(nomlangue__icontains=query)
        )

    return render(request, 'plate/cours.html', {'cours': cours, 'query': query})

@login_required
def detail(request, slug):
    # Récupérer le cours sélectionné
    cours = get_object_or_404(Cours, slug=slug)

    # Récupérer les cours associés à la langue du cours sélectionné
    dets = Cours.objects.filter(langue=cours.langue)

    return render(request, 'plate/cours/detail.html', {'cours': cours, 'dets': dets})

@login_required
def detail_lecon(request, slug, lecon_id):
    # Récupérer la leçon
    lecon = get_object_or_404(Leçon, id=lecon_id)

    # Récupérer le cours via le chapitre de la leçon
    cours = lecon.chap.cours

    # Vérifie si le cours a un slug
    if not cours.slug:
        cours.slug = slugify(f"{cours.titre}-{cours.langue.nomlangue}")
        cours.save()

    # Récupérer le contenu de la leçon
    vocabulaire = lecon.vocabulaire.all()
    dialogues = lecon.dialogues.all()
    exercices = lecon.exercices.all()
    jeux = lecon.jeux.all()

    # Débogage : Afficher les jeux dans la console
    #for jeu in jeux:
        #print(jeu.données)

    return render(request, 'plate/cours/detail_lecon.html', {
        'lecon': lecon,
        'cours': cours,
        'vocabulaire': vocabulaire,
        'dialogues': dialogues,
        'exercices': exercices,
        'jeux': jeux,
    })


def quiz(request, slug):
    # Récupérer la langue sélectionnée
    langue = get_object_or_404(Langue, slug=slug)

    # Récupérer les quiz associés à la langue
    quizzes = Quiz.objects.filter(langue=langue)

    # Récupérer un cours associé à cette langue (pour la navigation)
    cours = Cours.objects.filter(langue=langue).first()

    # Récupérer les scores des quiz pour l'utilisateur connecté
    user_scores = {score.quiz.id: score.stars for score in UserScore.objects.filter(user=request.user)}

    # Passer les données au template
    context = {
        'cours': cours,  # Ajout de l'objet cours
        'quizzes': quizzes,
        'user_scores': user_scores,  # Dictionnaire {quiz_id: étoiles}
    }
    return render(request, 'plate/cours/quiz.html', context)

def quiz_detail(request, quiz_id, slug):
    quiz = get_object_or_404(Quiz, slug=slug, id=quiz_id)
    questions = quiz.questions.all()
    cours = Cours.objects.filter(langue=quiz.langue).first()

    if request.method == 'POST':
        data = json.loads(request.body)  # Charger les données JSON envoyées par fetch
        score = 0
        incorrect_answers = []

        for question in questions:
            selected_answer_id = data.get(str(question.id))
            if selected_answer_id:
                selected_answer = Answer.objects.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1
                else:
                    correct_answer = question.answers.filter(is_correct=True).first()
                    incorrect_answers.append((question.text, correct_answer.text, selected_answer.text))

        total_questions = questions.count()

        # Attribution des étoiles
        if score == total_questions:
            stars = 3
        elif score >= total_questions * 0.66:
            stars = 2
        elif score >= total_questions * 0.34:
            stars = 1
        else:
            stars = 0

        # Enregistrement du score
        try:
            user_score, created = UserScore.objects.update_or_create(
                user=request.user,
                quiz=quiz,
                defaults={'score': score, 'stars': stars}
            )
        except Exception as e:
            print(f"Erreur lors de l'enregistrement : {e}")

        return JsonResponse({
            'score': score,
            'total_questions': total_questions,
            'incorrect_answers': incorrect_answers,
            'stars': stars
        })

    user_score = UserScore.objects.filter(user=request.user, quiz=quiz).first()
    user_stars = user_score.stars if user_score else 0

    return render(request, 'plate/cours/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
        'cours': cours,
        'user_stars': user_stars,
    })

def dico(request, slug):
    cours = get_object_or_404(Cours, slug=slug)
    dictionnaire_entries = Dictionnaire.objects.filter(langue_traditionnelle=cours.langue.nomlangue)

    result = None
    mot = request.GET.get('mot', '').strip()
    sens = request.GET.get('sens', 'fr-to-trad')

    print(f"🔍 Mot recherché: {mot}, Sens: {sens}, Langue: {cours.langue.nomlangue}")

    if mot:
        if sens == 'fr-to-trad':
            result = dictionnaire_entries.filter(mot_francais__iexact=mot).first()
        elif sens == 'trad-to-fr':
            result = dictionnaire_entries.filter(mot_traditionnel__iexact=mot).first()

    print("📌 Résultat trouvé:", result)

    context = {
        'cours': cours,
        'dictionnaire_entries': dictionnaire_entries,
        'result': result,
        'mot': mot,
        'sens': sens,
    }
    return render(request, 'plate/cours/dico.html', context)

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

@login_required
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

@login_required
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

@login_required
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

@login_required
def profil(request):
    user = request.user
    user_langues = request.user.langues.all()  # Récupérez les langues liées à l'utilisateur
    langues_disponibles = Langue.objects.all()

    if request.method == "POST":
        langue_id = request.POST.get('langue')
        if langue_id:
            try:
                nouvelle_langue = Langue.objects.get(id=langue_id)

                # Ajouter la langue
                if nouvelle_langue not in user.langues.all():
                    user.langues.add(nouvelle_langue)
                    user.save()

                # Ajouter les cours liés
                nouveaux_cours = Cours.objects.filter(langue=nouvelle_langue).exclude(id__in=user.cours_suivis.all())
                if nouveaux_cours.exists():
                    user.cours_suivis.add(*nouveaux_cours)
                    messages.success(request, f"Les cours de la langue {nouvelle_langue.nomlangue} ont été ajoutés.")
                else:
                    messages.warning(request, f"Aucun nouveau cours trouvé pour la langue {nouvelle_langue.nomlangue}.")
            except Langue.DoesNotExist:
                messages.error(request, "La langue sélectionnée n'existe pas.")

    # Récupérez les cours associés aux langues de l'utilisateur
    cours = Cours.objects.filter(langue__in=user.langues.all()).distinct()

    return render(request, 'plate/profile.html', {
        'user_langues': user_langues,
        'user': user,
        'langues_disponibles': langues_disponibles,
        'cours': cours,
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
