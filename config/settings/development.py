from .base import *
import os
from pathlib import Path

# Base directory setup
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(" ") + ["localhost", "127.0.0.1"]

