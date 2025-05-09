from django.contrib.auth.tokens import default_token_generator
from authentication.models import User
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from authentication.tasks.successful_registration_email import successful_registration_email

def activate(request, uidb64, token):
    try:
        # Decode the uidb64 to get the user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        # Validate the token
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            messages.success(request, "Profilingiz muvaffaqiyatli ro'yhatdan o'tdi va aktivlashtirildi.")
            # Send successful registration email
            successful_registration_email.delay(user.email, user.username, user.first_name, user.last_name)
            # Redirect to the frontend login page
            frontend_login_url = f"https://edvent.uz/signin"
            return redirect(frontend_login_url)  
        else:
            messages.error(request, "Aktivlashtirish linki noto'g'ri.")
            frontend_error_url = "https://edvent.uz"
            return redirect(frontend_error_url)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise Http404("Activation link is invalid.")
