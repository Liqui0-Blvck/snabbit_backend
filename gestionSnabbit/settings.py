from pathlib import Path
from datetime import timedelta
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-desarrollo-!=7s=imrh*+f$x22w9&p3o$%r1#h^$a&6u=8*(%=_lpxdnr!yj'
DEBUG = True


ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'cuentas.User'


# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
        
    ## REST FRAMEWORK y AUTH ###
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'djoser',
    'corsheaders',
    
    ### APPS ####
    
    'core.apps.CoreConfig',   
    'cuentas.apps.CuentasConfig', 
    'bd_ciudades', 
    
    ## APPS de Mejoras 
    'django_extensions',
    'simple_history',
    'import_export',
    
    
    


]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gestionSnabbit.urls'

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


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    #'backendsauth.bakenduserandemail.AuthentificationBackend',
    #'allauth.account.auth_backends.AuthenticationBackend',

]

WSGI_APPLICATION = 'gestionSnabbit.wsgi.application'
ASGI_APPLICATION = 'gestionSnabbit.asgi.application'




# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'db_comunas': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bd_comunachile',
        'USER': 'vpsprodal03',
        'HOST': '11.11.12.5',
        'PASSWORD': 'HQ@2hha34Dsf!J%',
        'PORT': 5432,
    },
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

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}



CORS_ORIGIN_ALLOW_ALL = True


# CORS_ALLOWED_ORIGINS = [
#     'https:11.11.12.8:3000',
# ]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATIOM': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATIOM': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'auth/restablecer-contraseña/confirmar/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'ACTIVATION_URL': 'auth/registro/verificacion-cuenta/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'EMAIL': {
        'activation': 'core.email.ActivationEmail',
        'password_reset': 'core.email.PasswordResetEmail',
    },
    'SERIALIZERS': {}
}
# GRAPH_MODELS = {
#     'all_applications': False,
#     'app_labels': ["iot",],
#     'group_models': False,
# }

SHELL_PLUS = "ipython"
# Additional IPython arguments to use
IPYTHON_ARGUMENTS = []

IPYTHON_KERNEL_DISPLAY_NAME = "Django Shell-Plus"

# Additional Notebook arguments to use
NOTEBOOK_ARGUMENTS = []
NOTEBOOK_KERNEL_SPEC_NAMES = ["python3", "python"]