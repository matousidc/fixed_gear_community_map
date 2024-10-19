from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfiles(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    bike = models.CharField(max_length=100, blank=True, null=True, default=None)
    instagram = models.URLField(max_length=100, blank=True, null=True, default=None)
    strava = models.URLField(max_length=100, blank=True, null=True, default=None)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to='profile-photos/', blank=True, null=True, default=None)


class BikePhoto(models.Model):
    user = models.ForeignKey(UserProfiles, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='bike_photos/')
    bike_model = models.CharField(max_length=100, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
