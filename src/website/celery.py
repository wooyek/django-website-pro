# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.

import logging
import os
from celery import Celery

import getpass
print("Celery user: %s" % getpass.getuser())


# determine where is the single absolute path that
# will be used as a reference point for other directories
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
logging.debug("os.environ['DJANGO_SETTINGS_MODULE']: %s" % os.environ['DJANGO_SETTINGS_MODULE'])

# from django.conf import settings
# settings._setup()
# logging.debug("settings.__dir__: %s", settings.__dir__())
# logging.debug("settings.DEBUG: %s", settings.DEBUG)


# Using Celery with Django
# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django

# set the default Django settings module for the 'celery' program.
app = Celery('website')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)






