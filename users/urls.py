from django.urls import path

from users import views

urlpatterns = [
    path("register", views.UserRegisterAPIView.as_view(), name="user_register"),
    path("activate", views.ActivateUserAPIView.as_view(), name="activate_user"),
    # path("verify", views.verify, name="verify"),
    path("login/", views.UserLoginAPIView.as_view(), name="user_login"),
    path("logout", views.UserLogoutAPIView.as_view(), name="user_logout"),
    # path("profile", views.profile, name="profile"),
    # path("email/change", views.email_change, name="email_change"),
    # path("password/reset", views.password_reset, name="password_reset"),
    # path("google/login", views.google_login, name="google_login"),
    # path("google/callback", views.google_callback, name="google_callback"),
    # path("binance/login", views.binance_login, name="binance_login"),
    # path("binance/callback", views.binance_callback, name="binance_callback"),
]
