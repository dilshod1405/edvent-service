from decouple import config
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',
    'social_django',
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    "authentication",
    "payment",
    "education",
    "payme",
    "django_filters",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

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


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']


MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMIN_INTERFACE_ENABLED = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}

AUTHENTICATION_BACKENDS = [
    'authentication.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

RESEND_API_KEY = config("RESEND_API_KEY")
RESEND_SENDER_EMAIL = config("RESEND_SENDER_EMAIL")


AUTH_USER_MODEL = "authentication.User"

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHOD = "email"


PAYME_ID = config("PAYME_ID")
PAYME_KEY = config("PAYME_KEY")
PAYME_ACCOUNT_FIELD = "id"
PAYME_AMOUNT_FIELD = "total_amount"
PAYME_ACCOUNT_MODEL = "payment.models.Transaction"
PAYME_ONE_TIME_PAYMENT = True

VDOCIPHER_API_SECRET = config("VDOCIPHER_API_SECRET")

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://www.edvent.uz',
    'https://edvent.uz',
    'http://localhost:5000',
]

CSRF_TRUSTED_ORIGINS = [
    'https://www.edvent.uz',
    'https://edvent.uz',
    'https://archedu.uz',
    'https://www.archedu.uz',
    'http://localhost:5000',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'chat.consumer': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

import logging
logging.getLogger("django.security.DisallowedHost").setLevel(logging.CRITICAL)


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True


JAZZMIN_SETTINGS = {
    "site_title": "Edvent.uz",
    "site_brand": "Edvent.uz",
    "welcome_title": "Edvent admin paneliga xush kelibsiz!",
    "site_icon": "images/e.png",
    "welcome_sign": "Edvent admin paneliga xush kelibsiz! Buyer faqat xodimlar uchun!",
    "copyright": "Edvent 2025",

    # Login sahifasi uchun LOGO
    "custom_css": "admin/css/custom.css",


    # Buttonlar rangi
    "button_classes": {
        "primary": "btn btn-outline-indigo",
        "danger": "btn btn-outline-danger",
        "success": "btn btn-success",
        "warning": "btn btn-warning",
        "info": "btn btn-info",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "show_jazzmin_version": False,
}