import requests
from celery import shared_task
from django.conf import settings

RESEND_API_URL = "https://api.resend.com/emails"
SENDER_EMAIL = settings.RESEND_SENDER_EMAIL
API_KEY = settings.RESEND_API_KEY

@shared_task
def send_activation_email(email, username, first_name, last_name, activation_link):
    subject = 'Edvent.uz - Profilingizni aktivlashtiring'

    # Plain text fallback
    body_text = f"""
Assalomu alaykum {first_name} {last_name},

Edvent.uz saytida ro‘yxatdan o‘tdingiz.
Profilingizni aktivlashtirish uchun quyidagi havolaga bosing:

{activation_link}

Agar bu xabar sizga noto‘g‘ri yuborilgan deb hisoblasangiz, iltimos e’tiborsiz qoldiring.

© 2025 Edvent.uz — Barcha huquqlar himoyalangan
"""

    body_html = f"""
<html>
  <body style="margin:0;padding:0;background-color:060a18;font-family:Arial,sans-serif;">
    <table align="center" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;margin:auto;background-color:060a18;padding:40px 20px;">
      <tr>
        <td style="color:#ffffff;text-align:center;">
          <h2>👋 Assalomu alaykum {first_name} {last_name}</h2>
          <p style="color:#cccccc;font-size:16px;">
            Edvent.uz saytida ro‘yxatdan o‘tdingiz. Profilingizni aktivlashtirish uchun quyidagi tugmani bosing:
          </p>
          <div style="margin:30px 0;">
            <a href="{activation_link}" target="_blank" style="background-color:#4F39F6;color:#ffffff;padding:14px 28px;text-decoration:none;font-weight:bold;font-size:16px;border-radius:8px;display:inline-block;">
              👉 {username} profilini aktivlashtirish
            </a>
          </div>
          <p style="font-size:14px;color:#999999;">
            Agar bu email noto‘g‘ri yuborilgan deb o‘ylasangiz, iltimos e’tiborsiz qoldiring.
          </p>
          <hr style="border:1px solid #333;margin:30px 0;">
          <p style="font-size:12px;color:#777777;">
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
                "headers": {
                    "List-Unsubscribe": f"<mailto:unsubscribe@edvent.uz>, <https://edvent.uz/unsubscribe>"
                }
            },
            headers={
                "Authorization": f"Bearer {API_KEY}"
            }
        )

        if response.status_code == 200:
            print("✅ Email muvaffaqiyatli yuborildi")
        else:
            print(f"❌ Email yuborishda xatolik: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Email yuborishda istisno: {e}")
