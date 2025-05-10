import requests
import logging
from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"
SENDER_EMAIL = getattr(settings, 'RESEND_SENDER_EMAIL', None)
API_KEY = getattr(settings, 'RESEND_API_KEY', None)

@shared_task
def successful_registration_email(email, username, first_name, last_name):
    subject = 'Edvent.uz - Muvaffaqiyatli ro‘yxatdan o‘tganingiz bilan!'

    # Plain text version for email clients that do not support HTML
    body_text = (
        f"Assalomu alaykum, {first_name} {last_name}!\n\n"
        "Siz Edvent.uz platformasida muvaffaqiyatli ro‘yxatdan o‘tdingiz.\n"
        "Endi barcha darslar, kurslar va imkoniyatlar siz uchun ochiq!\n\n"
        f"Profilga kirish: https://edvent.uz/signin\n\n"
        "Omad tilaymiz!\n\n"
        "Edvent.uz jamoasi"
    )

    # HTML version
    body_html = f"""
    <html>
      <body style="margin: 0; padding: 0; background-color: #060a18; font-family: Arial, sans-serif;">
        <table align="center" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: auto; padding: 40px 0;">
          <tr>
            <td bgcolor="#060a18" style="padding: 20px 30px; border-radius: 10px; color: #ffffff; font-family: Arial, sans-serif;">
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
                Ilmingiz ziyoda bo'lsin! 📚
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

    if not all([API_KEY, SENDER_EMAIL]):
        logger.error("RESEND_SENDER_EMAIL yoki RESEND_API_KEY sozlanmagan!")
        return

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
            },
            timeout=10
        )

        if response.status_code == 200:
            logger.info(f"Email '{subject}' to {email} sent successfully.")
        else:
            logger.error(f"Email yuborishda xatolik: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        logger.exception(f"Email yuborishda xatolik: {e}")
