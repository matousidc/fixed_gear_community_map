# Generated by Django 5.1.2 on 2024-10-28 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0011_alter_bikephoto_photo_alter_userprofiles_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofiles',
            name='bike',
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='about',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
