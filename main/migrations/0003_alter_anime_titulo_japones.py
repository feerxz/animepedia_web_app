# Generated by Django 4.2.7 on 2024-01-18 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_anime_titulo_ingles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='titulo_japones',
            field=models.CharField(max_length=80),
        ),
    ]