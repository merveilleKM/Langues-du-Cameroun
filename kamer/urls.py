from django.contrib import admin
from django.urls import path
from kamerapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name="accueil"),
    path('signin', views.signin),
    path('signup', views.signup),
    path('deconnect', views.deconnect),
    path('cours', views.cours),
    path('communaute', views.communaute),
    path('dashboard', views.dashboard),
    path('profil', views.profil),
    path('detail', views.detail),
    path('dico', views.dico),
    path('quiz', views.quiz),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
