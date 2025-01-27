from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('', views.accueil, name="accueil"),
    path('signin', views.signin),
    path('signup', views.signup),
    path('deconnect', views.deconnect),
    path('cours', views.cours, name="cours"),
    path('communaute', views.communaute, name="communaute"),
    path('dashboard', views.dashboard),
    
    path('profil', views.profil, name="profil"),
    path('update_profile/', views.update_profile, name='update_profile'),

    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('dico', views.dico, name="dico"),
    path('quiz', views.quiz, name="quiz"),

    path('publier/', views.publier, name='publier'),
    path('commentaire/', views.commentaire, name='commentaire'),
    path('add-comment/<int:notification_id>/', views.add_comment, name='add_comment'),
    path('search/', views.search, name='search'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)