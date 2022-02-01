import django_heroku
import os
import cloudinary
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('CODICE')

DEBUG = True

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

ADMINS = env('ADMINS')
MANAGERS = env('MANAGERS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'cloudinary',
    'cloudinary_storage',
    'psycopg2',
    'openpyxl',

    'captcha',
    'highcharts',
    'cryptography',
    'social_django',

    'django_countries',
    'crispy_forms',

    'anagrafica',
    'amministrazione',
    'accounts',
    'core',
    'frequenze'
]

cloudinary.config(
  cloud_name = 'hmrwrvhav',
  api_key = env('CLOUDINARY_KEY'),
  api_secret = env('CLOUDINARY_SECRET'),
  secure = True
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'hmrwrvhav',
    'API_KEY': env('CLOUDINARY_KEY'),
    'API_SECRET': env('CLOUDINARY_SECRET'),
}


CAPTCHA_FONT_SIZE = 40
CAPTCHA_IMAGE_SIZE = (280,70)
CAPTCHA_LENGTH = 5

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

CORS_ALLOWED_ORIGINS =[
    'http://localhost:19006',
    'http://localhost:19002'
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env('MAILGUN_USER')
EMAIL_HOST_PASSWORD = env('MAILGUN_KEY')


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'approval_prompt': 'force'
}

LOGIN_URL = '/complete/google-oauth2/'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'core.utils.first_access',
)

ROOT_URLCONF = 'gestionale_cfp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'core/templates/utils'),
                 os.path.join(BASE_DIR, 'accounts/templates'),
                 os.path.join(BASE_DIR, 'anagrafica/templates'),
                 os.path.join(BASE_DIR, 'core/templates'),
                 ],
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

WSGI_APPLICATION = 'gestionale_cfp.wsgi.application'

MOCK = True
if MOCK:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mock_db_gestionale_cfp',
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'db_gestionale_cfp',
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
# FIXTURE_DIRS = [os.path.join(BASE_DIR, 'anagrafica/fixtures'),
#                 ]

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'it'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static-storage')]

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-storage')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media-serve')
MEDIA_URL = '/media-serve/'

# Configure Django App for Heroku.

django_heroku.settings(locals())


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_log': {
            'level': 'DEBUG' if DEBUG else 'ERROR',  # invece di ERROR era INFO
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_log'],
            'level': 'DEBUG' if DEBUG else 'ERROR',  # invece di ERROR era INFO
            'propagate': True,
        },
    },
}


# LOG VIA MAIL
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'mail_admins': {
#         'level': 'ERROR',
#         'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }
