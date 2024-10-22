from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfiles, BikePhoto


class SignUpForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # TODO: create class Meta, but have test done before
    def save(self, commit=True):
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
        fields = ['name', 'city', 'country', 'bike', 'instagram', 'strava', 'profile_photo']


class BikePhotoForm(forms.ModelForm):
    class Meta:
        model = BikePhoto
        fields = ['user', 'photo', 'bike_model']
