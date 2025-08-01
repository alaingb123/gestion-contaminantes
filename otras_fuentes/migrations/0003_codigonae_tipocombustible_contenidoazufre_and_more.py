# Generated by Django 5.1.6 on 2025-02-27 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otras_fuentes', '0002_subordinacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoNAE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoCombustible',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContenidoAzufre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('porcentaje', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tipo_combustible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='otras_fuentes.tipocombustible')),
            ],
        ),
        migrations.CreateModel(
            name='ConsumoCombustible',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo_combustible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='otras_fuentes.tipocombustible')),
            ],
        ),
    ]
