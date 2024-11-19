# mycloud_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Пример корневого маршрута
def home(request):
    return HttpResponse("Welcome to the homepage!")

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка
    path('api/', include('mycloud_api.urls')),  # Подключение маршрутов API
    path('', home),  # Корневой маршрут
]
