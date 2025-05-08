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
      <body style="margin: 0; padding: 0; background-color: #0e0e16;">
        <table align="center" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: auto; padding: 40px 0;">
          <tr>
            <td bgcolor="#0e0e16" style="padding: 20px 30px; border-radius: 10px; color: #ffffff; font-family: Arial, sans-serif;">
              <h2 style="color: #ffffff; text-align: center;">👋 Assalomu alaykum {first_name} {last_name}</h2>
              <p style="font-size: 16px; color: #cccccc;">
                Edvent.uz saytida ro‘yxatdan o‘tdingiz. Profilingizni aktivlashtirish uchun quyidagi tugmani bosing:
              </p>
              <div style="text-align: center; margin: 30px 0;">
                <a href="{activation_link}" target="_blank" style="
                  background-color: #4F39F6;
                  color: #ffffff;
                  padding: 14px 28px;
                  text-decoration: none;
                  font-weight: bold;
                  font-size: 16px;
                  border-radius: 8px;
                  display: inline-block;
                ">
                  👉 Profilni Aktivlashtirish
                </a>
              </div>
              <p style="font-size: 14px; color: #999999;">
                Ushbu email noto‘g‘ri yuborilgan deb o‘ylasangiz, iltimos e’tiborsiz qoldiring.
              </p>
              <hr style="border: 1px solid #333; margin: 30px 0;">
              <p style="text-align: center; font-size: 12px; color: #777777;">
                © 2025 Edvent.uz — Barcha huquqlar himoyalangan
              </p>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """

    try:
        ses_client.send_email(
            Source=VERIFIED_FROM_EMAIL,
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Text': {'Data': body_text, 'Charset': 'UTF-8'},
                    'Html': {'Data': body_html, 'Charset': 'UTF-8'}
                }
            }
        )
    except Exception as e:
        print(f"Email yuborishda xatolik: {e}")


@shared_task
def successful_registration_email(email, username, first_name, last_name):
    subject = 'Edvent.uz - Muvaffaqiyatli ro‘yxatdan o‘tganingiz bilan!'
    
    body_text = ""
    
    body_html = f"""
    <html>
      <body style="margin: 0; padding: 0; background-color: #0e0e16;">
        <table align="center" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: auto; padding: 40px 0;">
          <tr>
            <td bgcolor="#0e0e16" style="padding: 20px 30px; border-radius: 10px; color: #ffffff; font-family: Arial, sans-serif;">
              <h2 style="color: #4F39F6; text-align: center;">🎉 Tabriklaymiz, {first_name} {last_name}!</h2>
              <p style="font-size: 16px; color: #cccccc; text-align: center;">
                Siz <strong>Edvent.uz</strong> platformasida muvaffaqiyatli ro‘yxatdan o‘tdingiz.<br>
                Endi barcha darslar, kurslar va imkoniyatlar siz uchun ochiq!
              </p>
              <div style="text-align: center; margin: 30px 0;">
                <a href="https://edvent.uz" target="_blank" style="
                  background-color: #4F39F6;
                  color: #ffffff;
                  padding: 14px 28px;
                  text-decoration: none;
                  font-weight: bold;
                  font-size: 16px;
                  border-radius: 8px;
                  display: inline-block;
                ">
                  🚀 {username} profilga o'tish
                </a>
              </div>
              <p style="font-size: 16px; color: #aaaaaa; text-align: center;">
                Edvent - zamonaviy kasblar kaliti!🔑
              </p>
              <hr style="border: 1px solid #333; margin: 30px 0;">
              <p style="font-size: 13px; color: #777777; text-align: center;">
                Agar bu email sizga noto‘g‘ri yuborilgan deb o‘ylasangiz, iltimos e’tiborsiz qoldiring.<br>
                &copy; 2025 Edvent.uz — Barcha huquqlar himoyalangan.
              </p>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """

    try:
        ses_client.send_email(
            Source=VERIFIED_FROM_EMAIL,
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Text': {'Data': body_text, 'Charset': 'UTF-8'},
                    'Html': {'Data': body_html, 'Charset': 'UTF-8'}
                }
            }
        )
    except Exception as e:
        print(f"Email yuborishda xatolik: {e}")

