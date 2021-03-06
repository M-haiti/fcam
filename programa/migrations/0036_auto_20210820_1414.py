# Generated by Django 3.2.6 on 2021-08-20 20:14

from django.db import migrations, models
import programa.models


class Migration(migrations.Migration):

    dependencies = [
        ('programa', '0035_auto_20210820_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupoactor',
            name='nombre',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='informefinal',
            name='estado_bancario',
            field=models.FileField(blank=True, null=True, upload_to='%Y/estadosbancarios', validators=[programa.models.validate_file_extension], verbose_name='Estado bancario (PDF)'),
        ),
        migrations.AlterField(
            model_name='informefinal',
            name='fecha_periodo_finit',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de finalización'),
        ),
        migrations.AlterField(
            model_name='informefinal',
            name='fecha_periodo_init',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de inicio'),
        ),
        migrations.AlterField(
            model_name='informefinal',
            name='fotografias',
            field=models.FileField(blank=True, null=True, upload_to='%Y/fotografias', validators=[programa.models.validate_file_extension], verbose_name='Fotografías'),
        ),
        migrations.AlterField(
            model_name='informefinal',
            name='reporte_financiero',
            field=models.FileField(blank=True, null=True, upload_to='%Y/reportesfinancieros', validators=[programa.models.validate_file_extension], verbose_name='Reporte Financiero (PDF)'),
        ),
        migrations.AlterField(
            model_name='informeintermedio',
            name='estado_bancario',
            field=models.FileField(blank=True, null=True, upload_to='%Y/estadosbancarios', validators=[programa.models.validate_file_extension], verbose_name='Estado bancario (PDF)'),
        ),
        migrations.AlterField(
            model_name='informeintermedio',
            name='fecha_periodo_finit',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de finalización'),
        ),
        migrations.AlterField(
            model_name='informeintermedio',
            name='fecha_periodo_init',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de inicio'),
        ),
        migrations.AlterField(
            model_name='informeintermedio',
            name='fotografias',
            field=models.FileField(blank=True, null=True, upload_to='%Y/fotografias', validators=[programa.models.validate_file_extension], verbose_name='Fotografías'),
        ),
        migrations.AlterField(
            model_name='informeintermedio',
            name='reporte_financiero',
            field=models.FileField(blank=True, null=True, upload_to='%Y/reportesfinancieros', validators=[programa.models.validate_file_extension], verbose_name='Reporte Financiero (PDF)'),
        ),
        migrations.AlterField(
            model_name='propuesta',
            name='fecha_aprobacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de aprobación'),
        ),
    ]
