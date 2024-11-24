from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)

class NoExpirationTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Exclude token check for the login page
        if request.path == '/api/auth/login/':  # Specify the path for your login endpoint
            return None  # No token check needed for the login page

        # Get the authorization header
        auth = self.get_authorization_header(request)
        if not auth:
            logger.warning("No authorization header found.")
            return None  # If the header is missing, there's no authentication

        token = auth.strip()  # Remove any extra spaces at the beginning and end

        # Check if the token exists
        if not token:
            logger.warning("Authorization header is empty.")
            raise AuthenticationFailed('No token provided.')

        # Log the token (this helps us understand what is going on)
        logger.debug("Received token: %s", token)

        # Insert your logic here to check and retrieve the user from the token
        user = self.get_user_from_token(token)
        if user is None:
            logger.error("Invalid token: %s", token)
            raise AuthenticationFailed('Invalid token.')

        return (user, token)  # Return a tuple with the user and token

    def get_authorization_header(self, request):
        """
        Returns the value of the Authorization header.
        """
        auth = request.headers.get('Authorization')
        return auth

    def get_user_from_token(self, token):
        """
        Logic for extracting the user from the token.
        This will need to be adjusted depending on your token mechanism.
        """
        try:
            # Look for the token in the database using DRF's Token model
            token_instance = Token.objects.get(key=token)
            logger.debug("Found user: %s for token: %s", token_instance.user.username, token)
            return token_instance.user  # Return the user associated with the token
        except Token.DoesNotExist:
            logger.error("Token not found: %s", token)
            return None
