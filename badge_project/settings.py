from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env', override=True)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,137.131.153.208"
).split(",")



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
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

ROOT_URLCONF = 'badge_project.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'badge_project.wsgi.application'
#DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "eventosflex"),
        "USER": os.environ.get("POSTGRES_USER", "eventos_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "Sys.Admin!@#098"),
        "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}



LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Maceio'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/organizacao/login/'
LOGIN_REDIRECT_URL = '/organizacao/'
LOGOUT_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/organizacao/login/'

EMAIL_MODE = os.getenv('EMAIL_MODE', 'console').lower()

if EMAIL_MODE == 'smtp':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.titan.email')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '465'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False').lower() in ('1', 'true', 'yes', 'on')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'True').lower() in ('1', 'true', 'yes', 'on')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'eventos@localhost.test')
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_TIMEOUT = 30

SITE_URL = os.getenv('SITE_URL', 'http://127.0.0.1:8000')


