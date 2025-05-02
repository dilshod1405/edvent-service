from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_activation_email(email, username, activation_link):
    send_mail(
        subject='Edvent.uz - Aktivlashtirish',
        message=f'Assalomu aleykum. Edvent.uz saytida foydalanuvchi {username}, profilingizni aktivlashtirish uchun quyidagi havolaga bosing: {activation_link}',
        from_email='www.edvent.uz@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def successful_registration_email(email, username):
    send_mail(
        subject='Edvent.uz - Tabriklaymiz !',
        message=f'Assalomu aleykum. Edvent.uz saytida foydalanuvchi {username} muvaffaqiyatli ro\'yxatdan o\'tdi.',
        from_email='www.edvent.uz@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )