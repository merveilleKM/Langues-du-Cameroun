# Generated by Django 5.1.5 on 2025-01-26 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kamerapp', '0007_auto_20250126_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='slug',
            field=models.SlugField(blank=True, default='Ewondo', unique=True),
        ),
    ]
