# Generated by Django 5.1.6 on 2025-03-05 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Contaminantes', '0018_remove_liquido_oace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='desechospeligroso',
            name='municipio',
        ),
    ]
