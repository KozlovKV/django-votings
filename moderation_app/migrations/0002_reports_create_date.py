# Generated by Django 3.1.4 on 2020-12-30 17:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('moderation_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
