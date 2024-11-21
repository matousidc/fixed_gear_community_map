from . import api_views
from django.urls import path

urlpatterns = [
    path("create-profile-api", api_views.CreateUserProfileView.as_view(), name="create-profile-api"),
    path("user-detail/<int:user_id>", api_views.ProfileDetailView.as_view(), name="user-detail-api"),
    path("profile-list", api_views.UserProfileListView.as_view(), name="profile-list")
]
