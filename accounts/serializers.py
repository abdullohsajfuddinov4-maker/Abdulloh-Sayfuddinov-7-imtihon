from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import EmailVerifyCode

User = get_user_model()

class RegisterRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password2", "phone_number", "address")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Email уже занят"})

        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"username": "Username уже занят"})

        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.is_active = False
        user.set_password(password)
        user.save()
        return user


class RegisterVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        email = attrs["email"]
        code = attrs["code"]

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({"email": "Пользователь не найден"})

        code_obj = (EmailVerifyCode.objects
                    .filter(user=user, is_used=False)
                    .order_by("-created_at")
                    .first())

        if not code_obj:
            raise serializers.ValidationError({"code": "Код не найден"})
        if code_obj.is_expired():
            raise serializers.ValidationError({"code": "Срок кода истёк"})
        if code_obj.code != code:
            raise serializers.ValidationError({"code": "Неверный код"})

        attrs["user"] = user
        attrs["code_obj"] = code_obj
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "phone_number", "address")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "phone_number", "address")


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        validate_password(value)
        return value


