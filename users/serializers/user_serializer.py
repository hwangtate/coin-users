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


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = User
        exclude = [
            "password",
        ]
        read_only_fields = [
            "id",
            "email",
            # "nickname", 이름 변경 가능
            # "password", 이미 exclude 에 포함 되어 있어서 read_only 임
            "social_provider",
            "ranking",
            "email_confirmed",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
            "updated_at",
            "last_login",
        ]


class UserChangeEmailSerializer(serializers.Serializer):
    old_email = serializers.EmailField()
    new_email = serializers.EmailField()

    def validate(self, data):
        old_email = data["old_email"]
        new_email = data["new_email"]

        user = self.context["user"]

        if user.email != old_email:
            raise ValidationError({"message": "Email doesn't match"})

        if old_email == new_email:
            raise ValidationError({"message": "Old email and New email must not match"})

        if User.objects.filter(email=new_email).exists():
            raise ValidationError({"message": "New Email already taken!"})

        return data

    def update(self, user, validated_data):
        user.email = validated_data.get("new_email")
        user.email_confirmed = False
        user.save()
        return user


class UserResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        old_password = data["old_password"]
        user = self.context["user"]

        if not user.check_password(old_password):
            raise ValidationError({"message": "Invalid password"})

        if old_password == data["password"] or old_password == data["password2"]:
            raise ValidationError({"message": "New password cannot be the same as the old password."})

        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match")

        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return data

    def update(self, user, validated_data):
        user.set_password(validated_data.get("password"))
        user.save()
        return user
