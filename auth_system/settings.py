import os
from pathlib import Path

from dotenv import load_dotenv
from drf_spectacular.utils import OpenApiExample

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
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
    'core.middleware.AuthMiddleware',
]

ROOT_URLCONF = 'auth_system.urls'

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

WSGI_APPLICATION = 'auth_system.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.User'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API системы',
    'DESCRIPTION': 'Кастомная аутентификация и авторизация',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

MOCK_PRODUCTS = [
    {'id': 1, 'name': 'Laptop', 'owner_id': 1},
    {'id': 2, 'name': 'Phone', 'owner_id': 2},
]
PRODUCT_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'owner_id': {'type': 'integer'},
        },
    },
}
USER_REQUEST_SCHEMA = {
    'application/json': {
        'type': 'object',
        'properties': {
            'email': {'type': 'string', 'format': 'email'},
            'password': {'type': 'string', 'minLength': 6},
        },
        'required': ['email', 'password'],
    },
}
USER_RESPONSES_SCHEMA = {
    200: {'type': 'object', 'properties': {'token': {'type': 'string'}}},
    401: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
}
USER_RESPONSES_SCHEMA_201 = {
    201: {'type': 'object', 'properties': {'message': {'type': 'string'}}},
}
EXAMPLES_LOGIN = [
    OpenApiExample(
        'Успешный вход',
        value={'email': 'admin@myapp.com', 'password': 'my_secure_pass'},
        request_only=True,
    ),
    OpenApiExample(
        'Ответ при успехе',
        value={'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'},
        response_only=True,
    ),
]
