from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from users.models import User


class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return None

        try:
            payload = decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            return (user_id, None)

        except (ExpiredSignatureError, InvalidTokenError, User.DoesNotExist):
            return None
