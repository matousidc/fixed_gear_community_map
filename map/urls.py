from django.urls import path
from . import views, api_views

urlpatterns = [
    path("", views.index_view, name="index"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-profile', views.create_profile_view, name='create-profile'),
    path('profile', views.profile_view, name='profile'),
    path('user-detail/<int:user_id>', views.user_detail_view, name='user-detail'),
    path('user-list', views.user_list_view, name='user-list'),
    path('manage-bikes', views.manage_bikes_view, name='manage-bikes'),
    path('delete-photo/<int:photo_id>', views.delete_bike_photo, name='delete-bike-photo'),
    path('upload-photo', views.upload_photo, name='upload-photo'),
    # api endpoints
    # path("create-profile-api", api_views.CreateUserProfileView.as_view(), name="create-profile-api"),
    # path("profile-list", api_views.UserProfileListView.as_view(), name="profile-list"),
    # path("profile-api", api_views.UserProfileView.as_view(), name="profile-api"), # not needed
    # path("user-detail/<int:user_id>", api_views.ProfileDetailView.as_view(), name="user-detail-api"),

]
