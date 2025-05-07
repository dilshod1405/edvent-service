from rest_framework import generics
from authentication.serializers.register_serializer import RegisterSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from authentication.tasks import send_activation_email

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        current_site = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"https://{current_site.domain}/authentication/activate/{uid}/{token}/"

        # Send activation email
        send_activation_email.delay(user.email, user.username, activation_link)
    