# Generated by Django 5.1.2 on 2024-10-16 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_alter_userprofiles_instagram_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='instagram',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='strava',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]
