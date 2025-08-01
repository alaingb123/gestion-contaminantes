# Generated by Django 5.1.6 on 2025-02-27 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contaminantes', '0006_parametrosatmosfera'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrosatmosfera',
            name='nh3_despues_tratamiento',
            field=models.CharField(choices=[('no_evalua', 'No se evalúa'), ('no_procede', 'No procede')], default='no_evalua', max_length=50),
        ),
        migrations.AlterField(
            model_name='parametrosatmosfera',
            name='nh3_emitido',
            field=models.CharField(choices=[('no_evalua', 'No se evalúa'), ('no_procede', 'No procede')], default='no_evalua', max_length=50),
        ),
        migrations.AlterField(
            model_name='parametrosatmosfera',
            name='nox_despues_tratamiento',
            field=models.CharField(choices=[('no_evalua', 'No se evalúa'), ('no_procede', 'No procede')], default='no_evalua', max_length=50),
        ),
        migrations.AlterField(
            model_name='parametrosatmosfera',
            name='nox_emitido',
            field=models.CharField(choices=[('no_evalua', 'No se evalúa'), ('no_procede', 'No procede')], default='no_evalua', max_length=50),
        ),
        migrations.AlterField(
            model_name='parametrosatmosfera',
            name='pm10_despues_tratamiento',
            field=models.CharField(choices=[('no_evalua', 'No se evalúa'), ('no_procede', 'No procede')], default='no_evalua', max_length=50),
        ),
        migrations.AlterField(
            model_name='parametrosatmosfera',
            name='pm10_emitido',
            field=models.CharField(choices=[('no_evalua', 'No se evalúa'), ('no_procede', 'No procede')], default='no_evalua', max_length=50),
        ),
        migrations.AlterField(
            model_name='parametrosatmosfera',
            name='pm_despues_tratamiento',
            field=models.CharField(choices=[('no_evalua', 'No se evalúa'), ('no_procede', 'No procede')], default='no_evalua', max_length=50),
        ),
        migrations.AlterField(
            model_name='parametrosatmosfera',
            name='pm_emitido',
            field=models.CharField(choices=[('no_evalua', 'No se evalúa'), ('no_procede', 'No procede')], default='no_evalua', max_length=50),
        ),
        migrations.AlterField(
            model_name='parametrosatmosfera',
            name='so2_despues_tratamiento',
            field=models.CharField(choices=[('no_evalua', 'No se evalúa'), ('no_procede', 'No procede')], default='no_evalua', max_length=50),
        ),
        migrations.AlterField(
            model_name='parametrosatmosfera',
            name='so2_emitido',
            field=models.CharField(choices=[('no_evalua', 'No se evalúa'), ('no_procede', 'No procede')], default='no_evalua', max_length=50),
        ),
    ]
