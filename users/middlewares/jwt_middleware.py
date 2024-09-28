from django.http import JsonResponse
from django.conf import settings
from jwt import decode, encode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from users.models import User
from users.services.jwt_service import generate_access_token


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header or not auth_header.startswith("Bearer "):
            return self.get_response(request)

        token = auth_header.split(" ")[1]

        try:
            payload = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            request.user = user
        except ExpiredSignatureError:
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                try:
                    refresh_payload = decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
                    user = User.objects.get(id=refresh_payload["user_id"])
                    new_access_token = generate_access_token(user)
                    response = self.get_response(request)
                    response.set_cookie(
                        "access_token",
                        new_access_token,
                        httponly=True,
                        samesite="Strict",
                    )
                    return response
                except (ExpiredSignatureError, InvalidTokenError):
                    return JsonResponse({"error": "Refresh token is invalid or expired"}, status=401)
            else:
                return JsonResponse({"error": "Access token expired and no refresh token provided"}, status=401)
        except InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return self.get_response(request)
