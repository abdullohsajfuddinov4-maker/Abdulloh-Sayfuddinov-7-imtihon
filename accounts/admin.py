from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,EmailVerifyCode


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Доп. поля", {"fields": ("phone_number", "address")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Доп. поля", {"fields": ("phone_number", "address")}),
    )
    list_display = ("username", "email", "phone_number", "is_staff")
admin.site.register(EmailVerifyCode)
