from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileForm, BikePhotoForm
from .models import UserProfiles, BikePhoto


def index(request):
    return HttpResponse("Hello, world. You're at the map index.")


# Sign-up view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Automatically log in the user after sign-up
            # Create a profile for the newly signed-up user
            UserProfiles.objects.create(user=user)
            return redirect('create-profile')  # Redirect to home page after sign-up
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# Login view using Django's built-in AuthenticationForm
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('profile')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def create_profile_view(request):
    profile = UserProfiles.objects.get(user=request.user)  # Get the current user's profile
    if request.method == 'POST':
        # instance= Prefill the form with the existing profile
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        bike_photo_form = BikePhotoForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_form.save()  # Save the updated profile

            for photo in request.FILES.getlist('photo'):
                BikePhoto.objects.create(user=profile, photo=photo,
                                         bike_model=bike_photo_form['bike_model'].value())
            return redirect('profile')  # Redirect to the profile view page
    else:
        profile_form = ProfileForm(instance=profile)  # Prefill the form with the current profile data
        bike_photo_form = BikePhotoForm()
    return render(request, 'create_profile.html', {'profile_form': profile_form, 'bike_photo_form': bike_photo_form})


@login_required
def profile_view(request):
    profile = UserProfiles.objects.get(user=request.user)  # Get the current user's profile
    bike_photos = BikePhoto.objects.filter(user=profile)
    return render(request, 'profile.html', {'profile': profile, 'bike_photos': bike_photos, 'user': request.user})


def user_detail_view(request, user_id):
    user = get_object_or_404(UserProfiles, user_id=user_id)
    bike_photos = BikePhoto.objects.filter(user=user)
    return render(request, 'profile.html', {'profile': user, 'bike_photos': bike_photos, 'user': request.user})


def user_list_view(request):
    users = UserProfiles.objects.all().order_by('name')
    return render(request, 'user_list.html', {'users': users})
