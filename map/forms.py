from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfiles, BikePhoto


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')  # , 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfiles
        fields = ['name', 'city', 'country', 'bike', 'instagram', 'strava', 'profile_photo']


class BikePhotoForm(forms.ModelForm):
    class Meta:
        model = BikePhoto
        fields = ['user', 'photo', 'bike_model']
