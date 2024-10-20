from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, api_views
from .views import signup, login_view

urlpatterns = [
    path("", views.index, name="index"),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Optional logout # todo: logout doesnt work
    path('create-profile', views.create_profile_view, name='create-profile'),
    path('profile', views.profile_view, name='profile'),
    path('user-detail/<int:user_id>', views.user_detail_view, name='user-detail'),
    path('user-list', views.user_list_view, name='user-list'),
    # api endpoints
    path("create-profile-api", api_views.CreateUserProfileView.as_view(), name="create-profile-api"),
    path("profile-list", api_views.UserProfileListView.as_view(), name="profile-list"),
    # path("profile-api", api_views.UserProfileView.as_view(), name="profile-api"), # not needed
    # path("user-detail/<int:user_id>", api_views.ProfileDetailView.as_view(), name="user-detail-api"),

]
