from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import  ProfileView, ProfileUpdateView, ResetPasswordView, LogoutView,RegisterRequestView,RegisterVerifyView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("profile/update/", ProfileUpdateView.as_view()),
    path("profile/reset-pass/", ResetPasswordView.as_view()),
    path("register/request/", RegisterRequestView.as_view()),
    path("register/verify/", RegisterVerifyView.as_view()),
]
