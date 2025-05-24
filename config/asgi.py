from decouple import config
import os
import django
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', config("DJANGO_SETTINGS_MODULE"))

# MUHIM: django.setup() avval bajariladi
django.setup()


application = get_asgi_application()