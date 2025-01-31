from django.contrib import admin
from .models import CustomUser, Ressource, Langue, Cours, Exercice, Expression,Progression,Leçon,Question,Quiz, UserScore, Notification,Answer, Dictionnaire, Chapitre

admin.site.register(CustomUser)
admin.site.register(Ressource)
admin.site.register(Langue)
admin.site.register(Cours)
admin.site.register(Exercice)
admin.site.register(Expression)
admin.site.register(Progression)
admin.site.register(Leçon)
admin.site.register(Chapitre)
admin.site.register(Question)
admin.site.register(Quiz)
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3  # Ajoute trois réponses par défaut

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'question_type')
    inlines = [AnswerInline]

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'level')

admin.site.register(UserScore)
admin.site.register(Notification)
admin.site.register(Answer)
admin.site.register(Dictionnaire)
