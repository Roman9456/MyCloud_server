from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)

class NoExpirationTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Исключаем проверку токена для страницы логина
        if request.path == '/api/auth/login/':  # Укажите путь для вашего эндпоинта авторизации
            return None  # Не нужно проверять токен для страницы логина

        # Получаем заголовок авторизации
        auth = self.get_authorization_header(request)
        if not auth:
            logger.warning("No authorization header found.")
            return None  # Если заголовок отсутствует, то аутентификации нет

        # Теперь не проверяем на "Bearer ", а сразу берем токен
        token = auth.strip()  # Убираем лишние пробелы в начале и в конце

        # Проверяем наличие токена
        if not token:
            logger.warning("Authorization header is empty.")
            raise AuthenticationFailed('No token provided.')

        # Логируем токен (это поможет нам понять, что происходит)
        logger.debug("Received token: %s", token)

        # Вставьте сюда вашу логику для проверки и извлечения пользователя из токена
        user = self.get_user_from_token(token)
        if user is None:
            logger.error("Invalid token: %s", token)
            raise AuthenticationFailed('Invalid token.')

        return (user, token)  # Возвращаем кортеж с пользователем и токеном

    def get_authorization_header(self, request):
        """
        Возвращает значение заголовка Authorization.
        """
        auth = request.headers.get('Authorization')
        return auth

    def get_user_from_token(self, token):
        """
        Логика для извлечения пользователя из токена.
        Это нужно будет настроить в зависимости от вашего механизма токенов.
        """
        try:
            # Ищем токен в базе данных с помощью Token модели из DRF
            token_instance = Token.objects.get(key=token)
            logger.debug("Found user: %s for token: %s", token_instance.user.username, token)
            return token_instance.user  # Возвращаем пользователя, связанного с токеном
        except Token.DoesNotExist:
            logger.error("Token not found: %s", token)
            return None
