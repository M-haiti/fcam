# Generated by Django 3.2.6 on 2021-08-16 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programa', '0017_auto_20210816_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apoyoestrategico',
            name='sitio_web',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='coparte',
            name='sitio_web',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='iniciativaconjunta',
            name='sitio_web',
            field=models.URLField(null=True),
        ),
    ]
