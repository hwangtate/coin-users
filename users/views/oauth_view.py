from django.contrib.auth import login
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import GOOGLE_CONFIG

from users.models import User
from users.permissions.user_permission import IsLoggedIn
from users.services.social_login_service import SocialLoginCallbackService, SocialLoginService


class GoogleLoginAPIView(APIView):
    permission_classes = (AllowAny, IsLoggedIn)

    gl = SocialLoginService()

    gl.login_uri = GOOGLE_CONFIG["LOGIN_URI"]
    gl.client_id = GOOGLE_CONFIG["CLIENT_ID"]
    gl.redirect_uri = GOOGLE_CONFIG["REDIRECT_URI"]

    scope = GOOGLE_CONFIG["SCOPE"]

    def get(self, request):
        return redirect(self.gl.social_login(context={"scope": self.scope}))


class GoogleLoginCallbackAPIView(APIView):
    permission_classes = (AllowAny, IsLoggedIn)

    glc = SocialLoginCallbackService()

    glc.client_id = GOOGLE_CONFIG["CLIENT_ID"]
    glc.client_secret = GOOGLE_CONFIG["CLIENT_SECRET"]
    glc.token_uri = GOOGLE_CONFIG["TOKEN_URI"]
    glc.profile_uri = GOOGLE_CONFIG["PROFILE_URI"]
    glc.redirect_uri = GOOGLE_CONFIG["REDIRECT_URI"]

    def get(self, request):
        token_request_data = self.glc.create_token_request_data(code=request.query_params.get("code", None))
        auth_headers = self.glc.get_auth_headers(token_request_data=token_request_data)
        user_data = self.glc.get_user_info(auth_headers=auth_headers)

        email = user_data["email"]
        nickname = user_data["name"]
        social_provider = "google"

        if User.objects.filter(email=email, social_provider=social_provider).exists():
            user = User.objects.get(email=email)
            login(request, user)

            return Response({"message": "login success"}, status=status.HTTP_200_OK)

        user = User.objects.create_social_user(email=email, nickname=nickname, social_provider=social_provider)
        login(request, user)

        return Response({"message": "register success"}, status=status.HTTP_200_OK)
