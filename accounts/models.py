from django.db import models
from django.contrib.auth.models import AbstractUser
from config import settings
from django.utils import timezone
from datetime import timedelta
import random

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='users',default='users/default.jpg', blank=True, null=True)


    def __str__(self):
        return self.username

class EmailVerifyCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="verify_codes")
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_code() -> str:
        return f"{random.randint(0, 999999):06d}"

    @classmethod
    def create_code(cls, user, ttl_minutes: int = 10):
        return cls.objects.create(user=user,code=cls.generate_code(),expires_at=timezone.now() + timedelta(minutes=ttl_minutes),)

    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at