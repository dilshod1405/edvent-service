from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

VERIFIED_FROM_EMAIL = settings.EMAIL_HOST_USER

@shared_task
def send_activation_email(email, username, activation_link):
    subject = 'Edvent.uz - Profilingizni aktivlashtiring'
    message = (
        f"Assalomu alaykum {username},\n\n"
        f"Edvent.uz saytida profilingizni aktivlashtirish uchun quyidagi havolaga bosing:\n"
        f"{activation_link}\n\n"
        f"Rahmat!"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=VERIFIED_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

@shared_task
def successful_registration_email(email, username):
    subject = 'Edvent.uz - Muvaffaqiyatli ro‘yxatdan o‘tganingiz bilan!'
    message = (
        f"Assalomu alaykum {username},\n\n"
        f"Tabriklaymiz! Siz Edvent.uz saytida muvaffaqiyatli ro‘yxatdan o‘tdingiz.\n"
        f"Endi siz platformamizdan to‘liq foydalanishingiz mumkin.\n\n"
        f"Omad tilaymiz!"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=VERIFIED_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


