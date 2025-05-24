from decouple import config
from .base import *
from pathlib import Path

# Base directory setup
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(" ")

CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', cast=bool, default=False)