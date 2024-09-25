from django.contrib.auth import login, logout, authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.permissions.user_permission import IsLoggedIn
from users.serializers.user_serializer import UserRegisterSerializer, UserLoginSerializer
from users.services.mail_service import EmailService
from users.services.user_service import UserService


class UserRegisterAPIView(APIView):
    permission_classes = (AllowAny, IsLoggedIn)
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
        activation_url = email_service.get_url(domain=f"{request.scheme}://{request.get_host()}", uri="/users/activate")
        email_service.send_register_mail(activation_url)

        data = {"success": True, "nickname": nickname, "email": email}

        return Response(data, status=status.HTTP_201_CREATED)


class ActivateUserAPIView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request):
        code = request.GET.get("code", "")
        email = EmailService.decode_signer(code)
        user = User.objects.get(email=email)

        user_service = UserService()
        user_service.user_email_confirmed(user)

        data = {"success": True, "nickname": user.nickname, "email": user.email}

        return Response(data, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=serializer.validated_data["email"])
        login(request, user)

        data = {
            "success": True,
            "email": serializer.data["email"],
        }

        return Response(data, status=status.HTTP_200_OK)


class UserLogoutAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        logout(request)

        data = {
            "success": True,
        }

        return Response(data, status=status.HTTP_200_OK)
