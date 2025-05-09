import requests
from celery import shared_task
from django.conf import settings

RESEND_API_URL = "https://api.resend.com/emails"
SENDER_EMAIL = settings.RESEND_SENDER_EMAIL
API_KEY = settings.RESEND_API_KEY

@shared_task
def successful_registration_email(email, username, first_name, last_name):
    subject = 'Edvent.uz - Muvaffaqiyatli ro‘yxatdan o‘tganingiz bilan!'

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
              <h2 style="color: #4F39F6; text-align: center;">🎉 Tabriklaymiz, {first_name} {last_name}!</h2>
              <p style="font-size: 16px; color: #cccccc; text-align: center;">
                Siz <strong>Edvent.uz</strong> platformasida muvaffaqiyatli ro‘yxatdan o‘tdingiz.<br>
                Endi barcha darslar, kurslar va imkoniyatlar siz uchun ochiq!
              </p>
              <div style="text-align: center; margin: 30px 0;">
                <a href="https://edvent.uz/signin" target="_blank" style="
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
                Omad tilaymiz va ilmingizga ilm qo‘shing! 📚
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

        if response.status_code == 200:
            print("Email muvaffaqiyatli yuborildi")
        else:
            print(f"Email yuborishda xatolik: {response.status_code}, {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Email yuborishda xatolik: {e}")
