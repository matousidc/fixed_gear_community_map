import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, Http404
from .forms import SignUpForm, LoginForm, ProfileForm, BikePhotoForm
from .models import UserProfiles, BikePhoto


def index_view(request):
    marker_coordinates = {}
    xx = UserProfiles.objects.filter(latitude__isnull=False)
    for x in xx:
        marker_coordinates[x.name] = {"latitude": x.latitude, "longitude": x.longitude,
                                      "popup_message": f"city: {x.city}, {x.country}",
                                      "profile": f"/map/user-detail/{x.user_id}"}
    return render(request, 'landing_page.html', {"marker": marker_coordinates})


# Sign-up view
def signup_view(request):
    template = 'signup_test.html'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'User with this email already exists.'
                })
            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                user = form.save()
                auth_login(request, user)  # Automatically log in the user after sign-up
                # Create a profile for the newly signed-up user
                UserProfiles.objects.create(user=user)
                return redirect('create-profile')  # Redirect to home page after sign-up
    else:
        form = SignUpForm()
    return render(request, template, {'form': form})


# Login view using Django's built-in AuthenticationForm
def login_view(request):
    template = 'login_test.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if not User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': "User with this email doesn't exist."
                })
            elif not User.objects.get(email=form.cleaned_data['email']).check_password(
                    form.cleaned_data['password']):
                return render(request, template, {
                    'form': form,
                    'error_message': 'Wrong password.'
                })
            else:
                auth_login(request, form.get_user())
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, template, {'form': form})


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('index')


@login_required
def create_profile_view(request):
    profile = UserProfiles.objects.get(user=request.user)  # Get the current user's profile
    if request.method == 'POST':
        # instance= Prefill the form with the existing profile
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            if profile_form.has_changed():
                # needed to get the instance without saving (commit=False) and update attributes
                user_profile = profile_form.save(commit=False)
                if 'city' in profile_form.changed_data:
                    resp = nominatim_api(request)
                    user_profile.latitude = resp[0]['lat']
                    user_profile.longitude = resp[0]['lon']
                user_profile.save()  # Save the updated profile
            return redirect('profile')  # Redirect to the profile view page
    else:
        profile_form = ProfileForm(instance=profile)  # Prefill the form with the current profile data
    return render(request, 'create_profile_test.html',
                  {'profile_form': profile_form})


def nominatim_api(request) -> dict:
    """Finds GPS location for the city user specified in the form"""
    location_url = f"https://nominatim.openstreetmap.org/search?q={request.POST['city']},{request.POST['country']}&format=json&limit=1"
    headers = {
        'User-Agent': 'Fixed gear community map',
        'email': 'matousslonek@gmail.com'
    }
    resp = requests.get(location_url, headers=headers)
    lat, lon = resp.json()[0]['lat'], resp.json()[0]['lon']
    bounding_box = resp.json()[0]['boundingbox']  # example: ['52.3382448', '52.6755087', '13.0883450', '13.7611609']
    # TODO: randomly place marker within the bounding box
    return resp.json()


@login_required
def manage_bikes_view(request):
    user = UserProfiles.objects.get(user=request.user)  # Get the current user's profile
    bike_photos = BikePhoto.objects.filter(user=user)
    if request.method == 'POST':
        bike_models = request.POST.getlist("bike_model")
        photo_order = request.POST.getlist("photo-order[]")
        # bike_photos.get(id=7)  # use this for indexing
        with transaction.atomic():
            for idx, photo_id in enumerate(photo_order):  # updating order for existing photos
                BikePhoto.objects.filter(id=int(photo_id)).update(display_order=idx, bike_model=bike_models[idx])

        bike_photo_form = BikePhotoForm(request.POST, request.FILES)  # new uploaded pics
        if bike_photo_form.is_valid():  # TODO: use form.save() override
            if bike_photo_form.has_changed():
                photo = request.FILES.get('photo')
                if photo:
                    BikePhoto.objects.create(user=user, photo=photo,
                                             bike_model=bike_photo_form.cleaned_data['bike_model'])
        return redirect('profile')  # Redirect to the profile view page
    else:
        bike_photo_form = BikePhotoForm()
    return render(request, 'manage_bikes.html', {'bike_photo_form': bike_photo_form, 'user_photos': bike_photos})


@login_required
def profile_view(request):
    profile = UserProfiles.objects.get(user=request.user)  # Get the current user's profile
    bike_photos = BikePhoto.objects.filter(user=profile)
    profile.create_instagram_username()
    return render(request, 'profile.html', {'profile': profile, 'bike_photos': bike_photos, 'user': request.user})


def user_detail_view(request, user_id: int):
    user = get_object_or_404(UserProfiles, user_id=user_id)
    bike_photos = BikePhoto.objects.filter(user=user)
    user.create_instagram_username()
    # TODO: logout is rendered even if user is not logged in
    return render(request, 'profile.html', {'profile': user, 'bike_photos': bike_photos, 'user': request.user})


def user_list_view(request: HttpRequest):
    users = UserProfiles.objects.all().order_by('name')
    return render(request, 'user_list.html', {'users': users})


@login_required
def delete_bike_photo(request, photo_id: int):
    try:
        user = UserProfiles.objects.get(user=request.user)
        photo = get_object_or_404(BikePhoto, id=photo_id, user=user)
    except Http404:  # handling deleting photos that don't belong to user or don't exist
        return redirect('manage-bikes')
    if request.method == 'POST':
        photo.delete()
    return redirect('manage-bikes')
