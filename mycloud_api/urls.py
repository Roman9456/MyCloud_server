from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FileViewSet, login_user, register_user, download_file_by_special_link

# Initialize the router and register the ViewSets for User and File
router = DefaultRouter()
router.register(r'users', UserViewSet)  # Registers the User ViewSet for user-related API endpoints
router.register(r'files', FileViewSet, basename='files')  # Registers the File ViewSet for file-related API endpoints

# Define the URL patterns
urlpatterns = [
    # Auth-related paths
    path('auth/login/', login_user, name='login_user'),  # User login path
    path('auth/register/', register_user, name='register_user'),  # User registration path

    # Download file by special link
    path('download/<str:special_link>/', download_file_by_special_link, name='download_file'),  # File download path using special link

    # Include the router URLs for the 'users' and 'files' endpoints
    path('', include(router.urls)),  # This will automatically include routes like /users/ and /files/
]
