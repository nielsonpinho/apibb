# Generated by Django 5.0.6 on 2024-06-03 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiBBs', '0002_pesquisa_usuario_alter_pesquisa_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesquisa',
            name='text',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pesquisa',
            name='usuario',
            field=models.CharField(max_length=100),
        ),
    ]
