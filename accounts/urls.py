from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegisterView, ProfileView, ProfileUpdateView, ResetPasswordView, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("profile/update/", ProfileUpdateView.as_view()),
    path("profile/reset-pass/", ResetPasswordView.as_view()),
]
