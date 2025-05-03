from .base import *
import os
from pathlib import Path

# Base directory setup
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
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

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'