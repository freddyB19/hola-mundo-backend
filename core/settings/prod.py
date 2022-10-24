import os

from .base import *

import dj_database_url
from corsheaders.defaults import default_methods, default_headers

SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)



# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://django_rf_game_user:9FJ5EX58n1LsAQQqgADyRrKdtaDHN9oY@dpg-cdbd60kgqg408qir7tng-a/django_rf_game',
        conn_max_age=600
    )}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOWED_ORIGINS = [
    "https://app-hola-mundo.vercel.app/"
]
# Una lista de orígenes confiables para solicitudes no seguras
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8080",
]

# Cors Methods
CORS_DEFAULT_METHODS = list(default_methods)

CORS_ADD_METHODS = []

CORS_ALLOW_METHODS =  CORS_DEFAULT_METHODS + CORS_ADD_METHODS


# Cors Headers
CORS_DEFAULT_HEADERS = list(default_headers)

CORS_ADD_HEADERS = [
    "content-disposition",
]


CORS_ALLOW_HEADERS = CORS_DEFAULT_HEADERS + CORS_ADD_HEADERS


STATIC_URL = 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media_root", "media")

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
