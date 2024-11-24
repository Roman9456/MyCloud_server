import os
import logging
from django.utils import timezone
from django.http import FileResponse, Http404, HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import UserFile, UserProfile
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, FileSerializer

logger = logging.getLogger(__name__)

User = get_user_model()

# Custom class for authentication
class CustomAuthentication(permissions.BasePermission):
    """
    Custom token check that allows working with the token even if it is invalid.
    """

    def has_permission(self, request, view):
        token_key = request.headers.get('Authorization')
        if token_key is None:
            return False

        # Extract token from "Authorization" header
        try:
            token = Token.objects.get(key=token_key.split(" ")[1])
            request.user = token.user  # Assign user from the token
        except Token.DoesNotExist:
            request.user = None
        return True

# User ViewSet with token check
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.
    """
    queryset = UserProfile.objects.all()  # Using UserProfile instead of User
    serializer_class = UserSerializer
    permission_classes = [CustomAuthentication]  # Using custom class for token check

    filterset_fields = ['id', ]
    search_fields = ['username', 'email']
    ordering_fields = ['id', 'username']

    @action(detail=False, methods=['get'], permission_classes=[CustomAuthentication])
    def me(self, request):
        logger.debug("Requesting user info: %s", request.user.username)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def list_users(self, request):
        logger.debug("Admin requesting user list: %s", request.user.username)
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        raise PermissionDenied("Access denied. You cannot view the user list.")

# File management with token check
class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [CustomAuthentication, IsOwnerOrReadOnly]  # Prevent unauthorized access

    filterset_fields = ['owner', 'original_filename', 'upload_date', 'last_downloaded', 'comment']
    search_fields = ['owner', 'original_filename', 'upload_date', 'last_downloaded', 'comment']
    ordering_fields = ['id', 'owner', 'original_filename', 'size', 'upload_date', 'last_downloaded', 'comment']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            user_id = self.request.query_params.get('user_id', None)
            if user_id:
                return UserFile.objects.filter(owner_id=user_id)
            return UserFile.objects.all()
        return UserFile.objects.filter(owner=user)

    def perform_create(self, serializer):
        try:
            logger.debug("Attempting file upload.")
            file_obj = self.request.FILES['file']  # Assuming 'file' is the key in the request
            original_name = file_obj.name
            size = file_obj.size
            user = self.request.user

            file_instance = UserFile(
                owner=user,
                original_filename=original_name,
                size=size,
                comment=self.request.data.get('comment', '')
            )
            file_instance.file = file_obj  # Store file in the FileField
            file_instance.save()
            logger.info("File '%s' successfully uploaded by user %s.", original_name, user.username)
            return Response(FileSerializer(file_instance).data, status=status.HTTP_201_CREATED)
        except KeyError:
            logger.warning("File not found in the request.")
            return Response({"detail": "File not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error during file upload: %s", str(e))
            return Response({"detail": "Error during file upload."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[CustomAuthentication])
    def my_files(self, request):
        logger.debug("Requesting files of user: %s", request.user.username)
        try:
            files = UserFile.objects.filter(owner=request.user)
            serializer = self.get_serializer(files, many=True)
            logger.info("User %s files successfully retrieved.", request.user.username)
            return Response(serializer.data)
        except ValidationError as e:
            logger.error(f"Error retrieving files: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsOwnerOrReadOnly])
    def rename_file(self, request, pk=None):
        logger.debug("Request to rename file with ID %s.", pk)
        try:
            file = self.get_object()
            new_name = request.data.get('new_name', None)

            if new_name:
                file.original_filename = new_name
                file.save(update_fields=['original_filename'])
                logger.info("File with ID %s renamed to '%s'.", pk, new_name)
            return Response(FileSerializer(file).data)
        except ValidationError as e:
            logger.error("Error renaming file with ID %s: %s", pk, str(e))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsOwnerOrReadOnly])
    def update_comment(self, request, pk=None):
        logger.debug("Request to update comment for file with ID %s.", pk)
        try:
            file = self.get_object()
            comment = request.data.get('comment', None)

            file.comment = comment
            file.save(update_fields=['comment'])
            serializer = self.get_serializer(file)
            logger.info("File with ID %s comment updated to '%s'.", pk, comment)
            return Response(serializer.data)
        except ValidationError as e:
            logger.error("Error updating comment for file with ID %s: %s", pk, str(e))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], permission_classes=[IsOwnerOrReadOnly])
    def download_file(self, request, pk=None):
        logger.debug("Request to download file with ID %s.", pk)
        try:
            file = self.get_object()
            response = FileResponse(open(file.file.path, 'rb'), as_attachment=True, filename=file.original_filename)
            file.last_downloaded = timezone.now()
            file.save()
            logger.info("File with ID %s successfully downloaded.", pk)
            return response
        except ValidationError as e:
            logger.error("Error downloading file with ID %s: %s", pk, str(e))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# API for downloading a file by a special link
@api_view(['get'])
def download_file_by_special_link(request, special_link):
    logger.debug("Request to download file by special link: %s", special_link)
    try:
        file_instance = UserFile.objects.get(special_link=special_link)
        file_path = file_instance.file.path

        if not os.path.exists(file_path):
            logger.warning("File not found by special link: %s", special_link)
            raise Http404("File not found.")

        file_instance.last_downloaded = timezone.now()
        file_instance.save()

        with open(file_path, 'rb') as f:
            logger.info("File with special link '%s' successfully downloaded.", special_link)
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{file_instance.original_filename}"'
            return response
    except UserFile.DoesNotExist:
        logger.error("File with special link '%s' not found.", special_link)
        raise Http404("File not found.")
    except Exception as e:
        logger.error("Error downloading file with special link '%s': %s", special_link, str(e))
        return Response({"detail": "Error downloading file."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API for user login with token
@api_view(['POST'])
def login_user(request):
    logger.debug("Attempting user login: %s", request.data.get('username'))
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        logger.info("User '%s' logged in successfully.", username)
        return Response({'token': token.key, 'username': user.username, 'email': user.email}, status=status.HTTP_200_OK)
    logger.error("Invalid credentials")
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# API for user registration with token
@api_view(['POST'])
def register_user(request):
    logger.debug("Registering new user: %s", request.data.get('username'))
    username = request.data.get('username')
    email = request.data.get('email')

    # Check if user already exists
    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        logger.warning("User with username '%s' or email '%s' already exists.", username, email)
        return Response({"detail": "A user with this username or email already exists."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Validate data with serializer
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        logger.info("User successfully created")

        # Create a token for the new user
        token, created = Token.objects.get_or_create(user=user)
        logger.info("Token for user created successfully")
        return Response({'token': token.key, **serializer.data}, status=status.HTTP_201_CREATED)

    # Return validation error
    logger.error("Validation error: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
