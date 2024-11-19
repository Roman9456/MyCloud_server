import os
import django
import jwt
from django.conf import settings

# Устанавливаем переменную окружения, чтобы Django знал, где находятся настройки
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mycloud.settings")

# Инициализируем Django
django.setup()

# Теперь можно использовать settings и другие компоненты Django
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxODQ4MTU0LCJpYXQiOjE3MzE4NDc4NTQsImp0aSI6ImVjYTFhODQzYjVmZTRiOWRiZjYxOGNiY2MzNDAxYjQzIiwidXNlcl9pZCI6NH0.cBY5vVnzNyBQ4cnro8j1UCY7LBGZrOBRgzVJJXKXCKc'

try:
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    print(decoded)  # Декодируем токен и проверяем содержимое
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError:
    print("Invalid token")