from django.shortcuts import render, redirect

def signin (request):
    return render(request, 'signin.html')

def signup (request):
    return render(request, 'signup.html')

def deconnect (request):
    return render(request, 'deconnect.html')

def accueil (request):
    return render(request, 'index.html')

def dashboard (request):
    return render(request, 'plate/dash.html')

def cours (request):
    return render(request, 'plate/cours.html')

def communaute (request):
    return render(request, 'plate/communaute.html')

def profil (request):
    return render(request, 'plate/profile.html')

def detail (request):
    return render(request, 'plate/cours/detail.html')

def dico (request):
    return render(request, 'plate/cours/dico.html')

def quiz (request):
    return render(request, 'plate/cours/quiz.html')

