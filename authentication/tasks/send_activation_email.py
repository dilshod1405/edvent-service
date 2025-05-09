import requests
from celery import shared_task
from django.conf import settings

RESEND_API_URL = "https://api.resend.com/emails"
SENDER_EMAIL = settings.RESEND_SENDER_EMAIL
API_KEY = settings.RESEND_API_KEY

# Celery task for sending activation email
@shared_task
def send_activation_email(email, username, first_name, last_name, activation_link):
    subject = 'Edvent.uz - Profilingizni aktivlashtiring'
    body_text = ""

    logo_url = "https://i.imgur.com/X9JjKcx.png"

    body_html = f"""
    <html>
      <body style="margin: 0; padding: 0; background-color: #0e0e16;">
        <table align="center" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: auto; padding: 40px 0;">
          <tr>
            <td style="text-align: center; padding-bottom: 20px;">
              <img src="{logo_url}" alt="Edvent Logo" width="150" />
            </td>
          </tr>
          <tr>
            <td bgcolor="#0e0e16" style="padding: 20px 30px; border-radius: 10px; color: #ffffff; font-family: Arial, sans-serif;">
              <h2 style="color: #ffffff; text-align: center;">👋 Assalomu alaykum {first_name} {last_name}</h2>
              <p style="font-size: 16px; color: #cccccc; text-align: center;">
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
                  👉 {username} profilini aktivlashtirish
                </a>
              </div>
              <p style="font-size: 14px; color: #999999; text-align: center;">
                Agar bu email noto‘g‘ri yuborilgan deb o‘ylasangiz, iltimos e’tiborsiz qoldiring.
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
        response = requests.post(
            RESEND_API_URL,
            json={
                "from": SENDER_EMAIL,
                "to": [email],
                "subject": subject,
                "html": body_html,
                "text": body_text,
            },
            headers={
                "Authorization": f"Bearer {API_KEY}"
            }
        )

        # API javobini tekshirish
        if response.status_code == 200:
            print("Email muvaffaqiyatli yuborildi")
        else:
            print(f"Email yuborishda xatolik: {response.status_code}, {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Email yuborishda xatolik: {e}")