from .models import UserProfiles, BikePhoto
from rest_framework import serializers


class CreateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfiles
        fields = ['user']


class UserProfileSerializer(serializers.ModelSerializer):
    country = serializers.ReadOnlyField(source='country.name')

    class Meta:
        model = UserProfiles
        fields = ['about', 'name', 'city', 'country', 'instagram', 'strava', 'profile_photo', 'created_at']
        read_only_fields = ['created_at']

    # Add validation for image upload
    def validate_profile_photo(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:  # Limit file size to 2MB
                raise serializers.ValidationError("Image size should not exceed 2MB.")
            return value


class BikePhotoSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = BikePhoto
        fields = ['user', 'photo', 'bike_model', 'created_at']
        read_only_fields = ['created_at']

    def validate_photo(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:  # Limit file size to 2MB
                raise serializers.ValidationError("Image size should not exceed 2MB.")
            return value
