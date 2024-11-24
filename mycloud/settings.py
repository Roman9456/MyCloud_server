import os
import sys
from pathlib import Path
import logging
from dotenv import load_dotenv

# Logging setup
logger = logging.getLogger(__name__)  # Moved logger creation here

# Load environment variables from .env file
load_dotenv()

# Path to the root of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')  # Secret key from environment variable

# Enable debug mode
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Hosts from which connections are allowed
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Applications that are active in the project
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'mycloud_api',  # Your API app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # For CORS handling
]

# Middleware for request processing
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Middleware for CORS handling
]

# URL configuration
ROOT_URLCONF = 'mycloud.urls'

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mycloud.wsgi.application'

# Database settings (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DJANGO_DB_NAME'),
        'USER': os.getenv('DJANGO_DB_USER'),
        'PASSWORD': os.getenv('DJANGO_DB_PASSWORD'),
        'HOST': os.getenv('DJANGO_DB_HOST', 'localhost'),
        'PORT': os.getenv('DJANGO_DB_PORT', 5432),
    }
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'storage': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Media file settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Local development site settings
if DEBUG:
    SITE_URL = 'http://127.0.0.1:8000'

# Django REST Framework settings
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'mycloud_api.exceptions.custom_exception_handler',  # Your custom exception handler
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'mycloud_api.authentication.NoExpirationTokenAuthentication',  # Your custom authentication class
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # Or use 'IsAuthenticated' if you need restricted access
    ),
    'SEARCH_PARAM': 'q',
    'ORDERING_PARAM': 'o',
}

# CORS (Cross-Origin Resource Sharing) settings
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5173').split(',')

if not CORS_ALLOWED_ORIGINS:
    logger.warning("CORS_ALLOWED_ORIGINS is empty, using default http://localhost:5173")
    CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]

CORS_ALLOW_CREDENTIALS = True  # Allow sending cookies and other data

# IP addresses for Django Debug Toolbar usage
INTERNAL_IPS = [
    "127.0.0.1",
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files settings
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Auto field configuration
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model configuration
AUTH_USER_MODEL = 'mycloud_api.UserProfile'

# Log settings loading
if DEBUG:
    logger.info("Django settings loaded successfully.")
else:
    logger.warning("Django settings loaded in production mode.")
