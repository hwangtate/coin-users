from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(serializers.Serializer):
    nickname = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match")

        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already registered")

        return data


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise ValidationError({"message": "Email doesn't exist!"})

        if not user.is_active:
            raise ValidationError({"message": "User is not active!"})

        if not user.check_password(password):
            raise ValidationError({"message": "Invalid password"})

        return data
