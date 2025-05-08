from celery import shared_task
import boto3
from django.conf import settings

VERIFIED_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
AWS_REGION = settings.AWS_REGION_NAME

# boto3 SES client yaratamiz
ses_client = boto3.client('ses', region_name=AWS_REGION)

@shared_task
def send_activation_email(email, username, activation_link):
    subject = 'Edvent.uz - Profilingizni aktivlashtiring'
    body_text = (
        f"Assalomu alaykum {username},\n\n"
        f"Edvent.uz saytida profilingizni aktivlashtirish uchun quyidagi havolaga bosing:\n"
        f"{activation_link}\n\n"
        f"Rahmat!"
    )

    try:
        ses_client.send_email(
            Source=VERIFIED_FROM_EMAIL,
            Destination={
                'ToAddresses': [email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
    except Exception as e:
        print(f"Email yuborishda xatolik: {e}")

@shared_task
def successful_registration_email(email, username):
    subject = 'Edvent.uz - Muvaffaqiyatli ro‘yxatdan o‘tganingiz bilan!'
    body_text = (
        f"Assalomu alaykum {username},\n\n"
        f"Tabriklaymiz! Siz Edvent.uz saytida muvaffaqiyatli ro‘yxatdan o‘tdingiz.\n"
        f"Endi siz platformamizdan to‘liq foydalanishingiz mumkin.\n\n"
        f"Omad tilaymiz!"
    )

    try:
        ses_client.send_email(
            Source=VERIFIED_FROM_EMAIL,
            Destination={
                'ToAddresses': [email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
    except Exception as e:
        print(f"Email yuborishda xatolik: {e}")
