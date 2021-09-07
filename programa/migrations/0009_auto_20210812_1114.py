# Generated by Django 3.2.6 on 2021-08-12 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('programa', '0008_auto_20210812_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contacto',
            name='organizacion',
        ),
        migrations.AddField(
            model_name='contacto',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='contacto',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
        ),
    ]