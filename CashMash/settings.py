"""
Django settings for SADAD project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os, datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm2g^b=@p60)yeuw3lzcg^hxdbdy5-ym2i#-_b+!xmbmll-(!hj'

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
     'rest_framework.authtoken',
     'CardManagement',
     'registerCard',
    'Consumer',
    'accounts',
    'APIKEY',
    'api',
    'EBS_CONSUMER_API',
    'otp'

]
THIRD_PARTY_APPS = ['import_export','rest_framework','corsheaders', 'rangefilter','phonenumber_field']
INSTALLED_APPS+=THIRD_PARTY_APPS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CashMash.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'CashMash.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CREATE USER 'CashMash'@'localhost' IDENTIFIED BY 'CashMash@2023##';
"""
#GRANT ALL PRIVILEGES ON *.* TO 'CashMash'@'localhost' WITH GRANT OPTION
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'CashMash',
        'USER': 'CashMash',
        'PASSWORD': 'CashMash@2023##',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }

}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         # mysql.connector.django
#         # 'ENGINE': 'mysql.connector.django',
#         'NAME': 'sadad',
#         'USER': 'sadad',
#         'PASSWORD': 'Sadad@payment##2021',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS': {
#           'autocommit': True,
#         },
        
#     }
# }
# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#             'OPTIONS' : {
#                 'read_default_file': '/etc/mysql/my.cnf',
#                 }
#             }
#         }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
      {
        'NAME': 'accounts.validators.CustomPasswordValidator',
    },
]
AUTH_USER_MODEL = 'accounts.User'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Africa/Khartoum'  
USE_TZ = True

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
EBS_CONSUMER_API = {
    'END_POINT': 'https://172.16.199.1:8877/QAConsumer',
    'APPLICATION_ID': 'ITQAN',
    'VERIFY_SSL': False,  # See line EBS_MERCHANT_API.VERIFY_SSL.
    'TIMEOUT': 60,  # 60 seconds
    'TIME_ZONE': 'Africa/Khartoum'  # This is used to parse datetime to the time zone EBS required
}
REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%d%m%y%H%M%S",
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
),
    
    
}



from corsheaders.defaults import default_headers

CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_REGEX_WHITELIST = ()

CORS_URLS_REGEX = r'^/consumer_api/.*$'

CORS_ALLOW_HEADERS = default_headers + (
    'API-KEY',
)
STATIC_ROOT = BASE_DIR / 'static'
#STATICFILES_DIRS = ( BASE_DIR / 'static')
JWT_AUTH = {
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_GET_USER_SECRET_KEY': 'Consumer.auth.utils.jwt_user_secret_handler',
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=1200),  # 20 minutes
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),

    'JWT_AUTH_HEADER_PREFIX': 'access_token',
    'JWT_AUTH_COOKIE': None,
}
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644
ADMIN_MEDIA_PREFIX = '/static/admin/'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATETIME_FORMAT = "%d%m%y%H%M%S"

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 