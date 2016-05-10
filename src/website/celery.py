# Copyright 2016 Janusz Skonieczny 

from __future__ import absolute_import

import logging
import sys
import os
from celery import Celery, signals

import getpass

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)

logging.info("Celery user: %s" % getpass.getuser())

# determine where is the single absolute path that
# will be used as a reference point for other directories
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
logging.info("os.environ['DJANGO_SETTINGS_MODULE']: %s" % os.environ['DJANGO_SETTINGS_MODULE'])

# Show a debugging info on console
logging.debug("__file__ = %s", __file__)
logging.debug("sys.version = %s", sys.version)
logging.debug("os.getpid() = %s", os.getpid())
logging.debug("os.getcwd() = %s", os.getcwd())
logging.debug("os.curdir = %s", os.curdir)
logging.debug("sys.path:\n\t%s", "\n\t".join(sys.path))
logging.debug("PYTHONPATH:\n\t%s", "\n\t".join(os.environ.get('PYTHONPATH', "").split(';')))
logging.debug("sys.modules.keys() = %s", repr(sys.modules.keys()))
logging.debug("sys.modules.has_key('website') = %s", 'website' in sys.modules)
if 'website' in sys.modules:
    logging.debug("sys.modules['website'].__name__ = %s", sys.modules['website'].__name__)
    logging.debug("sys.modules['website'].__file__ = %s", sys.modules['website'].__file__)

logging.debug("os.environ['DJANGO_SETTINGS_MODULE']= %s", os.environ.get('DJANGO_SETTINGS_MODULE', None))
from django.conf import settings

settings._setup()
logging.debug("settings.__dir__: %s", settings.__dir__())
logging.debug("settings.DEBUG: %s", settings.DEBUG)


# Using Celery with Django
# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django

# set the default Django settings module for the 'celery' program.
app = Celery('website.celery')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@signals.after_setup_logger.connect
def augment_logging_cfg(signal=None, sender=None, logger=None, loglevel=None, logfile=None, format=None, colorize=None):
    from django.utils.log import AdminEmailHandler
    handler = AdminEmailHandler()
    handler.level = logging.ERROR
    logger.handlers.append(handler)
