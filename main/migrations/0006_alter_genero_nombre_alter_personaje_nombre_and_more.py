# Generated by Django 4.2.7 on 2024-01-18 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_personaje_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genero',
            name='nombre',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='personaje',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='productor',
            name='nombre',
            field=models.CharField(max_length=80),
        ),
    ]