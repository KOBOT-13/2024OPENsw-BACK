"""
Django settings for ossKobot project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import json
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
with open(os.path.join(BASE_DIR, 'secret.json')) as f:
    secrets = json.load(f)

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured(f"The {setting} setting is missing in the secret.json file.")


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',  # 카카오 소셜 로그인
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # apps
    'books',
    'dialogs',
    'mypages',
    'quizzes',
    'users',
]

SITE_ID = 1

# 카카오톡 api
# SOCIALACCOUNT_PROVIDERS = {
#     'kakao': {
#         'APP': {
#             'client_id': '35e3a75771e92a596518518719f8d59f',
#             'secret': 'mOkb8h7AxH4XuZtfzi7VFSrOMMuv303r',
#             'key': ''
#         }
#     }
# }

REST_AUTH = {
    'USE_JWT' : True,
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_COOKIE' : "access_token",
    'JWT_AUTH_REFRESH_COOKIE' : "refresh_token",
    'JWT_AUTH_COOKIE_USE_CSRF' : True,
    'SESSION_LOGIN' : False
}

# SOCIALACCOUNT_LOGIN_ON_GET = True # 중간창이 뜨지 않고 카카오 로그인 페이지로 바로 이동
# LOGIN_REDIRECT_URL = 'main' # 로그인 완료 후 연결될 URL 설정.
# ACCOUNT_LOGOUT_REDIRECT_URL = 'index' # 로그아웃 후 연결될 URL 설정.
# ACCOUNT_LOGOUT_ON_GET = True # 로그아웃 요청시 즉시 로그아웃.

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none' # 필요하게 설정할꺼면 나중에 mandatory 로 바꾸면 됨.
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': '35e3a75771e92a596518518719f8d59f',
            'secret': 'mOkb8h7AxH4XuZtfzi7VFSrOMMuv303r',
            'key': ''
        }
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']
CSRF_COOKIE_HTTPONLY = False

ROOT_URLCONF = 'ossKobot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ossKobot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret("DB_NAME"),
        'USER': get_secret("DB_USER"),
        'PASSWORD': get_secret("DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'options': '-c client_encoding=UTF8'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

"""
# 배포 시 설정 변경
1. REST_FRAMEWORK의 DEFAULT_PERMISSION_CLASSES를 IsAuthenticaed로 바꾸기
2. CSRF 보호 활성화하기
    1) 미들웨어에 주석처리 되어있는 것 해제
    2) 배포 환경에 맞는 도메인 설정 : CSRF_TRUSTED_ORIGINS = ['https://your-production-domain.com']
    3) CSRF_COOKIE_HTTPONLY = True로 변경
3. DEBUG 모드 비활성화
    1) DEBUG = False
    2) ALLOWED_HOSTS = ['your-production-domain.com']
4. 보안 설정 강화

##### 보안 관련 설정입니다. 배포 시 주석 해제하고 설정해봅시다. #####

# SECURE_SSL_REDIRECT = True  # HTTPS 사용을 강제
# SESSION_COOKIE_SECURE = True  # HTTPS를 통해서만 쿠키 전송
# CSRF_COOKIE_SECURE = True  # HTTPS를 통해서만 CSRF 쿠키 전송
# SECURE_HSTS_SECONDS = 3600  # HSTS 사용 (1시간)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = 'DENY'
"""

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny', # 배포 시 AllowAny를 IsAuthenticated로 바꿉니다.
    ),
}



# 추가적인 JWT_AUTH 설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7), # 나중에 배포 전에 액세스 토큰 시간 줄이기 minutes=30
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
