# Generated by Django 3.1.4 on 2021-01-21 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0011_votings_votes_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votings',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='voting_images/'),
        ),
    ]
