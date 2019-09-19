"""
Django settings for gemtractor project.

Generated by 'django-admin startproject' using Django 1.11.22.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '!6qdx@dba$w9uh(6efjcnm_!gblg9i5_d^r&#8btxo=0na$b&)'
with open('secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
# TODO
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower () in ["true", "yes", "t", "y", "1"]

ALLOWED_HOSTS = ['localhost','127.0.0.1']
if "DJANGO_ALLOWED_HOSTS" in os.environ:
    ALLOWED_HOSTS.append (os.environ["DJANGO_ALLOWED_HOSTS"])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_nose',
    'index',
    'gemtract',
    'api'
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

ROOT_URLCONF = 'gemtractor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates'],
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

WSGI_APPLICATION = 'gemtractor.wsgi.application'

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=gemtractor,api,index,gemtract,modules.gemtractor',
]


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# allow for models up to 30mb
DATA_UPLOAD_MAX_MEMORY_SIZE=30*1024*1024

DJANGO_LOG_LEVEL = os.getenv('DJANGO_LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {name}:{module} [{levelname}]: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
        },
        'api': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
        },
        'gemtract': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
        },
        'index': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
        },
        'modules.gemtractor': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
        },
    },
}


# where to store uploaded/downloaded/generated stuff?
STORAGE = os.getenv('STORAGE_DIR', "/tmp/gemtractor-storage/")


import math
def parse_env_var (key, default):
  """
    parse some environment variable.
    
    will return the environmental value, unless its <= 0.
    if the value is <= 0, it will return infinity
    if the environment doesn't contain such a variable, it will return default
    
    Parameters
    ----------
    key : str
        the os' envirenment variable to evaluate
    default : int
        the default to return if the variable is not set

    Returns
    -------
    int
        the os' environment variable, or default, or infinity (if var <= 0)
  """
  val = float (os.getenv('KEEP_UPLOADED', default))
  if val <= 0:
    return math.inf
  return val


# how long to keep uploaded files
KEEP_UPLOADED = parse_env_var ('KEEP_UPLOADED', 1.5*60*60)
# how long to keep generated files (there are basically just for immediate download)
KEEP_GENERATED = parse_env_var ('KEEP_GENERATED', 10*60)

# how long to keep the bigg model list (that is the list of available models from bigg)
CACHE_BIGG = parse_env_var ('CACHE_BIGG', 60*60*24)
# how long to keep a single cached model obtained from bigg
CACHE_BIGG_MODEL = parse_env_var ('CACHE_BIGG_MODEL', 7*60*60*24)

# how long to keep the biomodel's search result
CACHE_BIOMODELS = parse_env_var ('CACHE_BIOMODELS', 60*60*24)
# how long to keep a single cached model from biomodels
CACHE_BIOMODELS_MODEL = parse_env_var ('CACHE_BIOMODELS_MODEL', 7*60*60*24)

# urls for model retrieval
URLS_BIGG_MODELS = "http://bigg.ucsd.edu/api/v2/models/"
URLS_BIGG_MODEL = lambda model_id: "http://bigg.ucsd.edu/static/models/"+model_id+".xml"
URLS_BIOMODELS = "https://www.ebi.ac.uk/biomodels/search?format=json&query=genome+scale+metabolic+model+modelformat%3A%22SBML%22+NOT+%22nicolas+le%22&numResults=100&sort=id-asc"
URLS_BIOMODEL_INFO = lambda model_id: "https://www.ebi.ac.uk/biomodels/"+model_id+"?format=json"
URLS_BIOMODEL_SBML = lambda model_id, filename: "https://www.ebi.ac.uk/biomodels/model/download/"+model_id+"?filename="+filename

# what's the max number of entities to allow in the browser
MAX_ENTITIES_FILTER = parse_env_var ('MAX_ENTITIES_FILTER', 100000)

