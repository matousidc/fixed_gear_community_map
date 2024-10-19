from .serializers import UserProfileSerializer, CreateUserProfileSerializer
from .models import UserProfiles
from rest_framework import generics, status, pagination, permissions, viewsets, filters
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser


class CreateUserProfileView(generics.CreateAPIView):
    queryset = UserProfiles.objects.all()
    serializer_class = CreateUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=request.user)
        except ValueError:
            raise PermissionDenied(detail="Only logged in users can create", code=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileListView(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfiles.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return CreateUserProfileSerializer
    #     return UserProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=request.user)
        except ValueError:
            raise PermissionDenied(detail="Only logged in users can create", code=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access
    parser_classes = [MultiPartParser, FormParser]  # Handle file uploads

    http_method_names = ['get', 'patch']

    def get_object(self):
        # Return the profile of the currently authenticated user
        return UserProfiles.objects.get(user=self.request.user)

    # Override the update method to ensure partial updates with PATCH
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Always use partial update
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        try:
            return UserProfiles.objects.get(user=self.kwargs['user_id'])
        except UserProfiles.DoesNotExist:
            raise NotFound(detail="User not found", code=status.HTTP_404_NOT_FOUND)