from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser


class IsEmailVerified(BasePermission):
    message = "Your email is not verified. Please verify your email to access this resource."

    def has_permission(self, request, view):
        return request.user


class IsLoggedIn(BasePermission):
    message = "Your account is logged in."

    def has_permission(self, request, view):
        if request.user is None:
            return False

        return False


class IsNotSocialUser(BasePermission):
    message = "Your account is social account. You can't change email or password."

    def has_permission(self, request, view):
        return request.user
