from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.permissions.user_permission import IsEmailVerified, IsLoggedIn, IsNotSocialUser
from users.serializers.user_serializer import (
    UserChangeEmailSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserResetPasswordSerializer,
    UserSerializer,
)
from users.services.jwt_service import generate_access_token, generate_refresh_token
from users.services.mail_service import EmailService
from users.services.user_service import UserService


class UserRegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        nickname = serializer.validated_data["nickname"]
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.create_user(nickname=nickname, email=email, password=password)

        email_service = EmailService(user)
        activation_url = email_service.get_url(domain=f"{request.scheme}://{request.get_host()}", uri="/users/verify")
        email_service.send_register_mail(activation_url)

        data = {"success": True, "nickname": nickname, "email": email}

        return Response(data, status=status.HTTP_201_CREATED)


class VerifyUserAPIView(APIView):

    def get(self, request):
        code = request.GET.get("code", "")
        email = EmailService.decode_signer(code)
        user = User.objects.get(email=email)

        user_service = UserService()
        user_service.user_email_confirmed(user)

        data = {"success": True, "nickname": user.nickname, "email": user.email}

        return Response(data, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=serializer.validated_data["email"])

        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)

        data = {
            "success": True,
            "email": serializer.data["email"],
            "access_token": access_token,
        }

        response = Response(data, status=status.HTTP_200_OK)
        # HttpOnly 쿠키에 refresh 토큰 저장
        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict")
        response.set_cookie("access_token", access_token, httponly=True, samesite="Strict")

        return response


class UserLogoutAPIView(APIView):

    def post(self, request):
        response = Response({"success": True}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")
        response.delete_cookie("sessionid")

        return response


class UserProfileAPIView(APIView):
    serializer_class = UserSerializer

    def get_user(self):
        if self.request.user == AnonymousUser():
            raise User.DoesNotExist
        user = User.objects.get(id=self.request.user)
        return user

    def get(self, request):
        try:
            user = self.get_user()
        except User.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = self.get_user()
        serializer = UserSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.update(user, serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = self.get_user()
        logout(request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserChangeEmailAPIView(APIView):
    serializer_class = UserChangeEmailSerializer

    def post(self, request):
        serializer = UserChangeEmailSerializer(data=request.data, context={"user": request.user})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=request.user.email)
        user = serializer.update(user, serializer.validated_data)

        email_service = EmailService(user)
        verification_url = email_service.get_url(domain=f"{request.scheme}://{request.get_host()}", uri="/users/verify")
        email_service.send_change_email_mail(verification_url)

        return Response(
            {
                "success": True,
                "email": serializer.data["new_email"],
            }
        )


class UserResetPasswordAPIView(APIView):

    serializer_class = UserResetPasswordSerializer

    def post(self, request):
        serializer = UserResetPasswordSerializer(data=request.data, context={"user": request.user})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        serializer.update(user, serializer.validated_data)

        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
