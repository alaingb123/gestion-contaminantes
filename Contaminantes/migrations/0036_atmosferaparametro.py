# Generated by Django 5.1.6 on 2025-04-24 02:43

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contaminantes', '0035_alter_desechospeligroso_entidad'),
        ('otras_fuentes', '0017_entidaddp'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtmosferaParametro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255)),
                ('prioridad', models.IntegerField(choices=[(1, 'Alta'), (2, 'Media'), (3, 'Baja')])),
                ('emisiones_no2', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('emisiones_so2', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('emisiones_pm10', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('emisiones_pm25', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('emisiones_co', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('emisiones_covdm', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('year', models.IntegerField(default=2025)),
                ('municipio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='otras_fuentes.municipio')),
                ('organismo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='otras_fuentes.oace')),
            ],
            options={
                'indexes': [models.Index(fields=['prioridad'], name='prioridadAP_idx')],
            },
        ),
    ]
