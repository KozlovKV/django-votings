# Generated by Django 3.1.4 on 2020-12-26 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote_app', '0002_votevariants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votings',
            name='CreationDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_vote', models.DateTimeField(auto_now_add=True)),
                ('Choices_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.votevariants')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('Votings_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.votings')),
            ],
        ),
    ]
