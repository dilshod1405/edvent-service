from .base import *

DEBUG = False


ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(" ")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

STATIC_ROOT = BASE_DIR / "config/staticfiles"
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / "config/media"
STATICFILES_DIRS = [BASE_DIR / "static"]