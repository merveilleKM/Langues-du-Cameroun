# Generated by Django 5.1.5 on 2025-02-11 10:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kamerapp', '0003_leçon_image_lecon_leçon_intro'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiviteRecente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_activite', models.CharField(choices=[('completed', 'Cours Terminé'), ('quiz', 'Quiz Répondu'), ('forum', 'Participation au Forum')], max_length=20)),
                ('description', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activite', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
