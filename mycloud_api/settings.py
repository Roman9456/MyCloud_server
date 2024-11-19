import os
from pathlib import Path

# Для использования файлов в пути
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ (изменить на свой для безопасности)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY',) # Получаем из переменной окружения

# Включите режим отладки для разработки
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Разрешенные хосты (для безопасности)
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,your-domain.com').split(',')

# Приложения Django
INSTALLED_APPS = [
    'mycloud_api',  # Ваше приложение
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Приложения для работы с API
    'rest_framework',
    'corsheaders',

    # Дополнительные приложения
    'simpleui',  # Пример административной панели
]

# Middleware для обработки CORS
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Для работы с CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

# Настройки базы данных PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DJANGO_DB_NAME', 'mycloud_db'),
        'USER': os.getenv('DJANGO_DB_USER', 'mycloud_user'),
        'PASSWORD': os.getenv('DJANGO_DB_PASSWORD', '417492178'),
        'HOST': os.getenv('DJANGO_DB_HOST', 'localhost'),
        'PORT': os.getenv('DJANGO_DB_PORT', '5432'),
    }
}

# Настройки для ограничения размера загружаемых файлов
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Настройки для работы с медиа-файлами (например, для загрузки файлов)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Папка для хранения медиа-файлов

# Статические файлы (например, для CSS, JS)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Папка для статических файлов

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Настройки для управления сессиями и куки
SESSION_COOKIE_AGE = 3600  # Время жизни сессии (1 час)
CSRF_COOKIE_SECURE = True  # Безопасность CSRF
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Файлы для хранения
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Логирование ошибок
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Для использования ASGI (если понадобится)
ASGI_APPLICATION = 'your_project_name.asgi.application'

# Для использования административной панели SimpleUI (если используется)
SIMPLEUI_HOME_INFO = False  # Отключаем информацию о SimpleUI на главной странице
SIMPLEUI_CONFIG = {
    'system_model_icon': True,
}

# Таймзона
TIME_ZONE = 'UTC'
USE_TZ = True

# Язык
LANGUAGE_CODE = 'en-us'

# Форматы
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'Y-m-d H:i:s'

# Прочие настройки безопасности
SECURE_SSL_REDIRECT = True  # Перенаправление на HTTPS
SECURE_HSTS_SECONDS = 3600  # Время действия заголовка HSTS (1 час)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Включаем поддомены в HSTS
SECURE_HSTS_PRELOAD = True  # Применяем HSTS на уровне браузеров

# Отключение дебаг-обработчика в продакшн
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Путь к файлу для загрузки (сильно зависит от вашего проекта)
ROOT_URLCONF = 'your_project_name.urls'

# Прочее
WSGI_APPLICATION = 'your_project_name.wsgi.application'

# Django-debug-toolbar (для разработки)
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1', 'localhost']