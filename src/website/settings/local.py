# coding=utf-8
# Created 2014 by Janusz Skonieczny
from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'data', 'db.dev.sqlite3'),
    }
}


# https://docs.djangoproject.com/en/1.6/topics/email/#console-backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

ASSETS_URL = STATIC_URL
ASSETS_MANIFEST = "json:{}".format(os.path.join(ASSETS_ROOT, "manifest.json"))
ASSETS_AUTO_BUILD = DEBUG

# Sync task testing
# http://docs.celeryproject.org/en/2.5/configuration.html?highlight=celery_always_eager#celery-always-eager

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
