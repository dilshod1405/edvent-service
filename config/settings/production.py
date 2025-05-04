from .base import *
from pathlib import Path

# Base directory setup
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
DEBUG = True
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
