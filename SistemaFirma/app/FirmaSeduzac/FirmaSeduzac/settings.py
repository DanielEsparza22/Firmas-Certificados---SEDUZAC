"""
Django settings for FirmaSeduzac project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as mensajes
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j2$)h9kvv*i&rko_xkz(r2f2qhg=pzym@1y(72&ftunx7h!obv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'FirmaCertificadosApp',
    'Login',
    'CertificacionesCompletasApp',
    'CertificacionesParcialesApp',
    'BachilleratoDistanciaApp',
    'PorEscuelaApp',
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

ROOT_URLCONF = 'FirmaSeduzac.urls'

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

WSGI_APPLICATION = 'FirmaSeduzac.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mariadb': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'migracion_certificaciones_seduzac',
        'USER': 'certuser',
        'PASSWORD': 'admin1234',
        'HOST': '192.168.33.10',
        'PORT': '3311',
    }
    # 'firebird': {
    #     'ENGINE': 'firebird',
    #     'NAME': '/firebird/data/certificacion.gdb',#pruebas
    #     # 'NAME': '/opt/data/certificacion.gdb',#producción
    #     'HOST': 'firebird2',
    #     'USER': 'SYSDBA',
    #     'PASSWORD': 'masterkey',
    #     'PORT': 3050,
    #     'OPTIONS': {
    #         'charset': 'latin1',
    #         'use_unicode': True,
    #     },
    # }
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

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración para media y estaticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

#CRISPY para forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Variables de sesión
LOGOUT_REDIRECT_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('Inicio')
LOGIN_URL = reverse_lazy('login')

# Tags para mensajes de exito, error etc.
MESSAGE_TAGS = {
    mensajes.DEBUG: 'debug',
    mensajes.INFO: 'info',
    mensajes.SUCCESS: 'succes',
    mensajes.WARNING: 'warning',
    mensajes.ERROR: 'danger',
}

