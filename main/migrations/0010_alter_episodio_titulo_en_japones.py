# Generated by Django 4.2.7 on 2024-01-18 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_episodio_titulo_en_japones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episodio',
            name='titulo_en_japones',
            field=models.CharField(max_length=255),
        ),
    ]
