from django.conf import global_settings

SECRET_KEY = '!DJANGO_JET_TESTS!'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = True

ROOT_URLCONF = 'jet.tests.urls'

INSTALLED_APPS = (
    'jet',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'jet.tests',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-US'
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_URL = '/static/'




