from django.urls import path

from users.views import oauth_view
from users.views import user_view as views

urlpatterns = [
    path("register", views.UserRegisterAPIView.as_view(), name="user_register"),
    path("login/", views.UserLoginAPIView.as_view(), name="user_login"),
    path("logout", views.UserLogoutAPIView.as_view(), name="user_logout"),
    path("profile", views.UserProfileAPIView.as_view(), name="user_profile"),
    path("email/change", views.UserChangeEmailAPIView.as_view(), name="user_email_change"),
    path("verify", views.VerifyUserAPIView.as_view(), name="verify_user"),
    path("password/reset", views.UserResetPasswordAPIView.as_view(), name="user_password_reset"),
    path("google/login", oauth_view.GoogleLoginAPIView.as_view(), name="google_login"),
    path("google/login/callback", oauth_view.GoogleLoginCallbackAPIView.as_view(), name="google_callback"),
    # path("binance/login", views.binance_login, name="binance_login"),
    # path("binance/callback", views.binance_callback, name="binance_callback"),
]
