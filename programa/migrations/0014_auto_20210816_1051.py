# Generated by Django 3.2.6 on 2021-08-16 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import programa.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('programa', '0013_auto_20210816_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformeIntermedio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plazo', models.CharField(choices=[('12M', '12 Meses'), ('18M', '18 Meses'), ('24M', '24 Meses'), ('36M', '36 Meses')], max_length=3, null=True, verbose_name='Duración de la propuesta')),
            ],
        ),
        migrations.RemoveField(
            model_name='propuesta',
            name='ano_convocatoria',
        ),
        migrations.AddField(
            model_name='propuesta',
            name='ano',
            field=models.CharField(choices=[('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025')], max_length=4, null=True, verbose_name='Año'),
        ),
        migrations.AlterField(
            model_name='propuesta',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reponsable_propu', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='propuesta',
            name='supervisora',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervisora_propu', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BaseInf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_periodo_init', models.DateField(null=True, verbose_name='Fecha de inicio')),
                ('fecha_periodo_finit', models.DateField(null=True, verbose_name='Fecha de finalización')),
                ('reporte_financiero', models.FileField(upload_to='', validators=[programa.models.validate_file_extension], verbose_name='Reporte Financiero (PDF):')),
                ('codigo_prop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='programa.propuesta')),
            ],
        ),
    ]
