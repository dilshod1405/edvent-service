from decouple import config
from .base import *
from pathlib import Path

# Base directory setup
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(" ")

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000', 'https://www.edvent.uz', 'https://edvent.uz', 'http://localhost:5000']
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000', 'https://www.edvent.uz', 'https://edvent.uz']
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', cast=bool, default=False)