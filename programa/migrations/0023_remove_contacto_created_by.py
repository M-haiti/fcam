# Generated by Django 3.2.6 on 2021-08-17 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programa', '0022_alter_contacto_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contacto',
            name='created_by',
        ),
    ]
