from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError  
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from .models import File  
from .serializers import FileSerializer 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import re
import logging

# Logging setup
logger = logging.getLogger(__name__) 

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer 



@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'status': 'fail', 'message': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Generate a new refresh token and access token for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'status': 'success',
            'message': 'Logged in successfully',
            'access_token': access_token  # Always provide a new token
        })

    # If authentication fails, return an error
    return Response({'status': 'fail', 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
def upload_file(request):
    # Логируем запрос на загрузку файла
    logger.info("Received file upload request.")
    
    # Указываем парсеры для обработки multipart-запросов
    parser_classes = [MultiPartParser, FormParser]

    try:
        # Проверяем и сохраняем файл
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            # Логируем успешную загрузку
            logger.info("File uploaded successfully.")
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Логируем ошибку валидации
            logger.error("File validation failed: %s", file_serializer.errors)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Логируем ошибку при загрузке файла
        logger.error(f"Error during file upload: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# User registration function
@api_view(['POST', 'GET'])
def register_user(request):
    logger.info(f"Received registration request: {request.data}")

    if request.method == 'GET':
        # Return instructions for registration
        return Response({
            'message': 'To register, send a POST request with username, email, and password.',
            'fields': ['username', 'email', 'password', 'fullName'],
        }, status=status.HTTP_200_OK)

    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        errors = {}

        # Field validation
        if not username:
            errors['username'] = 'Username is required.'
        if not email:
            errors['email'] = 'Email is required.'
        if not password:
            errors['password'] = 'Password is required.'

        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists.'
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists.'

        # Validate username with regex
        if username and not re.match(r'^[a-zA-Z0-9]{4,20}$', username):
            errors['username'] = 'Username must be between 4 and 20 characters and contain only letters and numbers.'

        # Validate email
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', email):
            errors['email'] = 'Invalid email format.'

        # Password validation
        if password and (len(password) < 6 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password) or not any(c in '!@#$%^&*()_+[]{}|;:,.<>?/~`' for c in password)):
            errors['password'] = 'Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character.'

        if errors:
            logger.error(f"Validation errors: {errors}")
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Create the user if all validations pass
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            logger.info(f"User registered successfully: {username}")
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error during user creation: {e}")
            return Response({"error": "Error during user creation: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Функция для получения нового токена по refresh токену
@api_view(['POST'])
def refresh_access_token(request):
    refresh_token = request.data.get('refresh_token')
    
    if not refresh_token:
        return Response({'status': 'fail', 'message': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Декодируем refresh токен
        refresh = RefreshToken(refresh_token)
        
        # Генерируем новый access токен
        access_token = str(refresh.access_token)
        
        return Response({
            'status': 'success',
            'access_token': access_token
        })
    except TokenError as e:
        return Response({'status': 'fail', 'message': 'Invalid or expired refresh token.'}, status=status.HTTP_400_BAD_REQUEST)