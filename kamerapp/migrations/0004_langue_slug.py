# Generated by Django 5.1.5 on 2025-01-26 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kamerapp', '0003_remove_cours_description_cours_slug_chapitre'),
    ]

    operations = [
        migrations.AddField(
            model_name='langue',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
