
import os
import dj_database_url
from decouple import config
from celery.schedules import crontab
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^m#u%f&ym-&e)ejf1h!28e*z-3uy9s_2mx=_91g)mw5*15b#pq'

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
    ###
    'bot',
    'sitemonitor',
    'rest_framework',
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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

try:
    SECRET_KEY = config('SECRET_KEY')

    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL')
        )
    }
except:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'uptimbo_db',
            'USER': 'postgres',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


PAGE_ACCESS_TOKEN = "EAADblDInlO4BAKaAvEN6OMEK71nZA5w9x8FwSbgDzPDtj0ANVXqzlAFTQkWwHVekEX7WxjrGFJZABJZBka3MiiXYgoXYQcZAqqa9rXWKFkQ3xvbyGRalZCn1azISVAvUxxCTYw3HGofmKMSMJSvMJF48BZAKZBfqxBieWYPDhcqBAZDZD"

VERIFY_TOKEN = "IAmGroot"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "project/static"),
]


#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


host = config('host')
if host == "PRODUCTION":
    LOAD_SDK = True
    WEB_VIEW_URL = "https://uptimbo.ruhshan.xyz/sitemonitor/add"
    SITE_LIST_URL = "https://uptimbo.ruhshan.xyz/sitemonitor/list/"
    SITE_DETAIL_URL = "https://uptimbo.ruhshan.xyz/sitemonitor/sitedetail/"
else:
    host = 'local'
    LOAD_SDK = False
    WEB_VIEW_URL = "http://localhost:8000/sitemonitor/add"
    SITE_LIST_URL = "http://localhost:8000/sitemonitor/list/"
    SITE_DETAIL_URL = "http://localhost:8000/sitemonitor/sitedetail/"


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
    'PATCH',
)

#BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'
