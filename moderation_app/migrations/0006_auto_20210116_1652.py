# Generated by Django 3.1.4 on 2021-01-16 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation_app', '0005_auto_20210116_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
