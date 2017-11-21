"""
Django settings for spravka11 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r3=ema_ir*1=@obx0t7hm0+v9ug$vizq)_a@d9*arx$b11h5vt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'haystack',
    'news',
    'events',
    'company',
    'mptt',
    'banners',
    'sorl.thumbnail',
    'import_export',
    'disqus',
    'vizitka',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'utils.subdomain.CompanySiteMiddleware',
)

ROOT_URLCONF = 'spravka11.urls'

WSGI_APPLICATION = 'spravka11.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_PATH = os.path.join(BASE_DIR,'static')

STATIC_URL = '/static/' # You may find this is already defined as such.

STATICFILES_DIRS = (
    STATIC_PATH,
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.request',

    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    'utils.subdomain.main_domain_context_processor',
)


GRAPPELLI_INDEX_DASHBOARD = 'spravka11.dash.CustomIndexDashboard'

GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS = {
    'myapp': {
        'Company': ('id__iexact', 'name__icontains',)
        }
    }

MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/home/spravka/projects/spravka11/media/cache/site',
    }
}

CACHE_MIDDLEWARE_SECONDS = 10#900

DISQUS_API_KEY = '7cPmQiwg4VFzhIAk9lpBdsazji3NRILFQx3zkKCOuhyt0UrUDL57z22fr27hYRZU'
DISQUS_WEBSITE_SHORTNAME = 'spravkakomi11'

MAIN_DOMAIN = 'spravka11.ru'

try:
    from .local_settings import *
except ImportError:
    pass