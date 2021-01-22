# Generated by Django 3.1.4 on 2021-01-22 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote_app', '0013_auto_20210121_2015'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteChangeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('voting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.votings')),
            ],
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.IntegerField(choices=[(0, 'Жалоба на голосование'), (1, 'Сообщение об ошибке')], default=0)),
                ('element', models.IntegerField(blank=True, null=True)),
                ('content', models.TextField()),
                ('status', models.IntegerField(choices=[(0, 'Обрабатывается'), (1, 'Решена'), (2, 'Отклонена')], default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('close_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
