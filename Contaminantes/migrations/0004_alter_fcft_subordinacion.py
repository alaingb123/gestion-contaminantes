# Generated by Django 5.1.6 on 2025-02-22 22:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contaminantes', '0003_fcft'),
        ('otras_fuentes', '0002_subordinacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fcft',
            name='subordinacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='otras_fuentes.subordinacion'),
        ),
    ]
