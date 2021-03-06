# Generated by Django 3.2.6 on 2021-08-16 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa', '0016_auto_20210816_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='apoyoestrategico',
            name='programa',
            field=models.CharField(choices=[('AFP', 'AfroPoderosas'), ('DMJ', 'Derechos de las Mujeres y Justicia Ambiental'), ('DLM', 'Derechos Laborales de las Mujeres'), ('DSR', 'Derechos Sexuales y Reproductivos'), ('LDS', 'Liderando desde el Sur'), ('MDC', 'Mujeres con Discapacidad'), ('MMJ', 'Mujeres jóvenes'), ('MMM', 'Mujeres Migrantes'), ('PEG', 'Programa Especial Guatemala'), ('NIN', 'Ninguno')], max_length=3, null=True, verbose_name='Programa'),
        ),
        migrations.AddField(
            model_name='iniciativaconjunta',
            name='programa',
            field=models.CharField(choices=[('AFP', 'AfroPoderosas'), ('DMJ', 'Derechos de las Mujeres y Justicia Ambiental'), ('DLM', 'Derechos Laborales de las Mujeres'), ('DSR', 'Derechos Sexuales y Reproductivos'), ('LDS', 'Liderando desde el Sur'), ('MDC', 'Mujeres con Discapacidad'), ('MMJ', 'Mujeres jóvenes'), ('MMM', 'Mujeres Migrantes'), ('PEG', 'Programa Especial Guatemala'), ('NIN', 'Ninguno')], max_length=3, null=True, verbose_name='Programa'),
        ),
        migrations.AlterField(
            model_name='propuesta',
            name='programa',
            field=models.CharField(choices=[('AFP', 'AfroPoderosas'), ('DMJ', 'Derechos de las Mujeres y Justicia Ambiental'), ('DLM', 'Derechos Laborales de las Mujeres'), ('DSR', 'Derechos Sexuales y Reproductivos'), ('LDS', 'Liderando desde el Sur'), ('MDC', 'Mujeres con Discapacidad'), ('MMJ', 'Mujeres jóvenes'), ('MMM', 'Mujeres Migrantes'), ('PEG', 'Programa Especial Guatemala'), ('NIN', 'Ninguno')], max_length=3, null=True, verbose_name='Programa'),
        ),
    ]
