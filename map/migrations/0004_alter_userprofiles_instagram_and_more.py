# Generated by Django 5.1.2 on 2024-10-16 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_userprofiles_instagram_userprofiles_strava'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='instagram',
            field=models.URLField(blank=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofiles',
            name='strava',
            field=models.URLField(blank=None, max_length=100, null=True),
        ),
    ]