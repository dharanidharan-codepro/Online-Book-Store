
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
    load_dotenv(BASE_DIR.parent / '.env')
except ImportError:
    pass

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or os.environ.get('SECRET_KEY', 'django-insecure-harbour-books')
DEBUG = (os.environ.get('DJANGO_DEBUG') == '1') or (os.environ.get('DEBUG', 'True').lower() in ('true', '1'))
_allowed = os.environ.get('DJANGO_ALLOWED_HOSTS') or os.environ.get('ALLOWED_HOSTS', '*')
ALLOWED_HOSTS = ['*'] if _allowed == '*' else [h.strip() for h in _allowed.split(',') if h.strip()]
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://localhost',
]

SITE_NAME = 'Harbour Books'
SITE_TAGLINE = 'Books, sellers, and thoughtful reading.'
PROMO_TITLE = 'Summer reading starts here'
PROMO_SUBTITLE = 'Browse new releases, hidden gems, and the best value on every page.'
SUPPORT_EMAIL = 'support@harbourbooks.test'
SOCIAL_LINKS = {'instagram': 'https://instagram.com', 'facebook': 'https://facebook.com', 'x': 'https://x.com'}
DELIVERY_MIN_DAYS = int(os.environ.get('DELIVERY_MIN_DAYS', '2'))
DELIVERY_MAX_DAYS = int(os.environ.get('DELIVERY_MAX_DAYS', '7'))
DELIVERY_SKIP_SUNDAY = os.environ.get('DELIVERY_SKIP_SUNDAY', 'false').lower() == 'true'

# --- AI summary (Google Gemini) ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '').strip()
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-3.5-flash').strip()
GEMINI_TIMEOUT = max(int(os.environ.get('GEMINI_TIMEOUT', '15')), 10)  # at least 10s for generation

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog',
    'accounts',
    'cart',
    'newsletter',
    'ai_summary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'harbour_books.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            # Global cart count injected into every template
            'cart.context_processors.cart_globals',
        ],
    },
}]

WSGI_APPLICATION = 'harbour_books.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
