from rest_framework.permissions import BasePermission


class IsEmailVerified(BasePermission):
    message = "Your email is not verified. Please verify your email to access this resource."

    def has_permission(self, request, view):
        return request.user and request.user.email_confirmed


class IsLoggedIn(BasePermission):
    message = "Your account is logged in."

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsNotSocialUser(BasePermission):
    message = "Your account is social account. You can't change email or password."

    def has_permission(self, request, view):
        return request.user.social_provider is None
