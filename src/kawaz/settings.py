"""
Django settings for Kawaz project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import sys
REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xd(wr812awpkuu4+7o)#ugb)*a0z!-m^an+m)%ly$l(ses8_g1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_comments',
    'rest_framework',
    'permission',
    'thumbnailfield',
    'roughpages',
    'registration',
    'crispy_forms',
    'compressor',
    'kawaz.core.management',
    'kawaz.core.db',
    'kawaz.core.utils',
    'kawaz.core.personas',
    'kawaz.core.publishments',
    'kawaz.core.registrations',
    'kawaz.core.forms',
    'kawaz.core.templatetags',
    'kawaz.core.gcal',
    'kawaz.apps.activities',
    'kawaz.apps.activities.contrib.hatenablog',
    'kawaz.apps.announcements',
    'kawaz.apps.attachments',
    'kawaz.apps.profiles',
    'kawaz.apps.projects',
    'kawaz.apps.events',
    'kawaz.apps.blogs',
    'kawaz.apps.products',
    'kawaz.apps.stars',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'roughpages.middleware.RoughpageFallbackMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'permission.backends.PermissionBackend',
)

ROOT_URLCONF = 'kawaz.urls'

WSGI_APPLICATION = 'kawaz.wsgi.application'

# validation_on_save decorator (kawaz.core.db.decorators)
# To disable automatical validation, set this variable to False
VALIDATE_ON_SAVE_DISABLE = False

AUTH_USER_MODEL = 'personas.Persona'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(REPOSITORY_ROOT, 'db.sqlite3'),
    }
}

THUMBNAIL_SIZE_PATTERNS = {
    'huge': (288, 288,),
    'large': (96, 96,),
    'middle': (48, 48,),
    'small': (24, 24,),
}

PRODUCT_THUMBNAIL_SIZE_PATTERNS = {
    None : (32, 32),
}

ADVERTISEMENT_IMAGE_SIZE_PATTERNS = {
    None : (32, 32),
}

SCREENSHOT_IMAGE_SIZE_PATTERNS = {
    None : (32, 32),
}

# Permission presence check in DEBUG mode
# from django-permission 0.5.3
PERMISSION_CHECK_PERMISSION_PRESENCE = DEBUG

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ja'

gettext = lambda s: s
LANGUAGES = (
    ('en-us', gettext('English')),
    ('ja', gettext('Japanese')),
)

LOCALE_PATHS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'kawaz', 'locale'),
)

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)

LOGIN_URL = '/registration/login/'
LOGOUT_URL = '/registration/logout/'
LOGIN_REDIRECT_URL = '/'

MEDIA_URL = '/storage/'
MEDIA_ROOT = os.path.join(REPOSITORY_ROOT, 'public', 'storage')

STATIC_URL = '/statics/'
STATIC_ROOT = os.path.join(REPOSITORY_ROOT, 'public', 'statics')
STATICFILES_DIRS = (
    os.path.join(REPOSITORY_ROOT, 'src', 'statics'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
)

# inspectional-registration
REGISTRATION_SUPPLEMENT_CLASS = (
    'kawaz.core.registrations.models.RegistrationSupplement')
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_DJANGO_AUTH_URLS_ENABLE = False

# rest-framework
DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

TEST_RUNNER = 'kawaz.core.tests.runner.KawazDiscoverRunner'
TESTING = False

RECENT_ACTIVITY_FEED_URL = 'http://kawazinfo.hateblo.jp/rss'
ACTIVITIES_HATENABLOG_FEED_URL = 'http://kawazinfo.hateblo.jp/rss'

SITE_ID = 1

# Google Calendar Synchronize
GCAL_CALENDAR_ID = (
    # DEBUG用カレンダー
    'kawaz.org_u41faouova38rcoh8eaimbg42c@group.calendar.google.com'
)
GCAL_EVENT_MODEL = 'events.Event'
GCAL_BACKEND_CLASS = 'kawaz.apps.events.gcal.KawazGoogleCalendarBackend'
GCAL_CLIENT_SECRETS = os.path.join(
    REPOSITORY_ROOT, 'config', 'gcal', 'client_secrets.json')
GCAL_CREDENTIALS = os.path.join(
    REPOSITORY_ROOT, 'config', 'gcal', 'credentials.json')


# crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap3', 'crispy')

if DEBUG:
    # テスト時のRuntimeWarningをexceptionにしている
    # https://docs.djangoproject.com/en/dev/topics/i18n/timezones/#code
    import warnings
    warnings.filterwarnings(
        'error', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')


# 環境依存の設定（デプロイサーバー固有の設定など）を読み込む
LOCAL_SETTINGS_LOADED = False

# DjangoのMessageをBootstrap3に適応させている
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

try:
    from .local_settings import *
except ImportError:
    pass
