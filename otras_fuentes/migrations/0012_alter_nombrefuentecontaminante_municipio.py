# Generated by Django 5.1.6 on 2025-03-05 19:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otras_fuentes', '0011_nombrefuentecontaminante_municipio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nombrefuentecontaminante',
            name='municipio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='otras_fuentes.municipio'),
        ),
    ]
