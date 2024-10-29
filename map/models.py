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
    about = models.TextField(blank=True, null=True, default=None)
    name = models.CharField(max_length=100, blank=True, null=True, default=None)
    city = models.CharField(max_length=100, blank=True, null=True, default=None)
    country = models.CharField(max_length=100, blank=True, null=True, default=None)
    instagram = models.URLField(max_length=100, blank=True, null=True, default=None)
    strava = models.URLField(max_length=100, blank=True, null=True, default=None)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to='profile-photos/', blank=True, null=True, default=None)

    def create_username(self):
        """Parse only username from instagram link"""
        if self.instagram:
            if not self.instagram.split("/")[-1]:
                self.instagram_username = '@' + self.instagram.split("/")[-2]
            else:
                self.instagram_username = "@" + self.instagram.split("/")[-1]


class BikePhoto(models.Model):
    user = models.ForeignKey(UserProfiles, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='bike_photos/', blank=True, null=True, default=None)
    bike_model = models.CharField(max_length=100, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        """Delete the photo file from storage"""
        if self.photo:
            self.photo.delete(save=False)
        # Call the superclass delete method to remove the instance from the database
        super().delete(*args, **kwargs)
