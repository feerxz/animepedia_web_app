# Generated by Django 4.2.7 on 2024-01-18 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_genero_nombre_alter_personaje_nombre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episodio',
            name='titulo_episodio',
            field=models.CharField(max_length=100),
        ),
    ]
