# Generated by Django 5.0.6 on 2024-07-08 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0006_alter_actor_character_alter_movie_plot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title_kor',
            field=models.CharField(max_length=50),
        ),
    ]
