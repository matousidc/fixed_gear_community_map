from django import forms
from django.contrib.auth.models import User
from .models import UserProfiles, BikePhoto


class SignUpForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['email'].split('@')[0],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password1'])
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def get_user(self):
        return User.objects.get(email=self.cleaned_data['email'])


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfiles
        fields = ['about', 'name', 'city', 'country', 'instagram', 'strava', 'profile_photo']

    def save(self, commit=True):
        """Delete the old profile photo if a new one is uploaded"""
        if (self.instance.pk and self.cleaned_data['profile_photo'] and
                self.cleaned_data['profile_photo'] != self.instance.profile_photo):
            old_profile_photo = UserProfiles.objects.get(pk=self.instance.pk).profile_photo
            if old_profile_photo:
                old_profile_photo.delete(save=False)
        return super().save(commit)


class BikePhotoForm(forms.ModelForm):
    class Meta:
        model = BikePhoto
        fields = ['photo', 'bike_model', 'display_order']

    # def save(self, commit=True):
    #     bike_photo = BikePhoto.objects.create(user=self.user, photo=photo, bike_model=bike_photo_form.cleaned_data['bike_model'])
