# Generated by Django 5.0.6 on 2024-07-08 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_actor_character'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='director',
            new_name='director_name',
        ),
    ]