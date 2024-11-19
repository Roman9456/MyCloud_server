from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mycloud_api.views import login_user, register_user, FileViewSet, refresh_access_token
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_file



router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Для получения access токена
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Для обновления access токена
    path('', include(router.urls)),  # Все маршруты, связанные с файлами, будут здесь 
    path('refresh-token/', refresh_access_token, name='refresh-token'),  # Маршрут для обновления токена
    path('api/files/upload/', upload_file, name='upload-file'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
