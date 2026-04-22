
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, VerifyOTPView, LoginView, ProfileView

urlpatterns = [
    path("auth/register/",   RegisterView.as_view()),
    path("auth/verify-otp/", VerifyOTPView.as_view()),
    path("auth/login/",      LoginView.as_view()),
    path("auth/refresh/",    TokenRefreshView.as_view()),
    path("profile/",         ProfileView.as_view()),
]