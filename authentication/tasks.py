from celery import shared_task
import boto3
from django.conf import settings

VERIFIED_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
AWS_REGION = settings.AWS_REGION_NAME

# boto3 SES client yaratamiz
ses_client = boto3.client('ses', region_name=AWS_REGION)

@shared_task
def send_activation_email(email, username, first_name, last_name, activation_link):
    subject = 'Edvent.uz - Profilingizni aktivlashtiring'
    body_text = ""
    body_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
          <h2 style="color: #4F39F6;">Assalomu alaykum {first_name} {last_name},</h2>
          <p style="font-size: 16px; color: #333;">
            Siz <strong style="color: #4F39F6;">Edvent.uz</strong> saytida ro‘yxatdan o‘tdingiz. <strong style="color: #4F39F6;">{username}</strong> profilingizni aktivlashtirish uchun quyidagi tugmani bosing:
          </p>
          <div style="text-align: center; margin: 30px 0;">
            <a href="{activation_link}" target="_blank" style="background-color: #4F39F6; color: #fff; padding: 14px 24px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 16px;">
              Profilni Aktivlashtirish
            </a>
          </div>
          <p style="font-size: 14px; color: #666;">Agar siz bu emailni xato olgan bo‘lsangiz, iltimos e’tiborsiz qoldiring.</p>
          <hr style="margin: 30px 0;">
          <p style="font-size: 12px; color: #aaa;">© 2025 Edvent.uz — Barcha huquqlar himoyalangan.</p>
        </div>
      </body>
    </html>
    """
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
                    },
                    'Html': {
                        'Data': body_html,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
    except Exception as e:
        print(f"Email yuborishda xatolik: {e}")

@shared_task
def successful_registration_email(email, username, first_name, last_name):
    subject = 'Edvent.uz - Muvaffaqiyatli ro‘yxatdan o‘tganingiz bilan!'
    body_html = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
      <h2 style="color: #4CAF50;">Assalomu alaykum {first_name} {last_name},</h2>
      <p style="font-size: 16px; color: #333;">
        <strong>Tabriklaymiz!</strong> Siz <strong>Edvent.uz</strong> saytida muvaffaqiyatli ro‘yxatdan o‘tdingiz.
        Endi siz bizning platformamizdan to‘liq foydalanishingiz mumkin.
      </p>
      <p style="font-size: 16px; color: #333;">Omad tilaymiz va ilmingizga ilm qo‘shing! 📚</p>
      <hr style="margin: 30px 0;">
      <p style="font-size: 14px; color: #999;">Agar bu email sizga xato kelgan bo‘lsa, iltimos, biz bilan bog‘laning.</p>
      <p style="font-size: 14px; color: #999;">&copy; 2025 Edvent.uz | Barcha huquqlar himoyalangan.</p>
    </div>
  </body>
</html>
"""
    body_text = ""  # Define body_text as an empty string

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
                    },
                    'Html': {
                        'Data': body_html,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
    except Exception as e:
        print(f"Email yuborishda xatolik: {e}")
