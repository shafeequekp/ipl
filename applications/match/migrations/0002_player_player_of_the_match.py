# Generated by Django 3.2.13 on 2023-02-10 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='player_of_the_match',
            field=models.IntegerField(default=0),
        ),
    ]
