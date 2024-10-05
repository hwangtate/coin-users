from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache

from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from users.services.jwt_service import generate_access_token

"""
과연 JsonResponse로 리턴 하는게 맞을까?
아니면 raise로 에러를 일으키는게 맞을까? 
"""


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get("access_token")
        if not token:
            return self.get_response(request)

        try:
            decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        except ExpiredSignatureError:
            user_id = decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})["user_id"]
            refresh_token = cache.get(f"refresh_token_{user_id}")

            if refresh_token:
                try:
                    refresh_payload = decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
                    new_access_token = generate_access_token(refresh_payload["user_id"])
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
