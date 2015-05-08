
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(SETTINGS_DIR + "/../..")
GIT_DIR = os.path.abspath(PROJECT_DIR + "/..")

# Where we want to store static files.
STATIC_ROOT = GIT_DIR + "/static/"
STATIC_URL = "/static/"

# We keep our static source files in the "static" directory.
STATICFILES_DIRS = [os.path.join(PROJECT_DIR, "static")]

# We keep our template files in the project "template" directory.
TEMPLATE_DIRS = (os.path.join(PROJECT_DIR, "templates"),)

DEFAULT_FROM_EMAIL = 'joel@joelburton.com'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'


# Email these people when errors happen on production sites

ADMINS = (('Joel', 'joel@joelburton.com'), )
SERVER_EMAIL = "joel@joelburton.com"


DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

DBBACKUP_DATE_FORMAT = ''
DBBACKUP_BACKUP_DIRECTORY = GIT_DIR + '/backups/'


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'appbunny.urls'

WSGI_APPLICATION = 'appbunny.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'appbunny',
        'HOST': 'localhost'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True