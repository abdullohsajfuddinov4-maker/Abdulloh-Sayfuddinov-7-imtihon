
from django.conf import settings
from django.core.mail import send_mail

def send_register_code(email: str, code: str):
    send_mail(
        subject="tastiqlash kodi",
        message=f"code {code}\nishlash muddati",
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None) or settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
