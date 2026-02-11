from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import permissions
from .utils import send_register_code
from .serializers import (
    RegisterRequestSerializer,
    EmailVerifyCode,
    ProfileSerializer,
    ProfileUpdateSerializer,
    RegisterVerifySerializer,
    ResetPasswordSerializer,
)





User = get_user_model()

class RegisterRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        code_obj = EmailVerifyCode.create_code(user=user, ttl_minutes=10)
        send_register_code(user.email, code_obj.code)

        return Response(
            {"detail": "kod yuborildi", "email": user.email},
            status=status.HTTP_201_CREATED
        )


class RegisterVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        code_obj = serializer.validated_data["code_obj"]

        user.is_active = True
        user.save(update_fields=["is_active"])

        code_obj.is_used = True
        code_obj.save(update_fields=["is_used"])

        return Response({"detail": "royhattan otdingiz "}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ProfileSerializer(request.user).data)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        if not request.user.check_password(old_password):
            return Response(
                {"old_password": "eski password mos emas"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.set_password(new_password)
        request.user.save(update_fields=["password"])

        return Response({"detail": "parol yangilandi"}, status=status.HTTP_200_OK)




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        refresh = request.data["refresh"]
        if not refresh:
            return Response({'massage':'refresh majbury'})

        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            return Response({'massage':'notogri refresh tokin'},status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "siz tizimdan chiqildingiz."}, status=status.HTTP_200_OK)


