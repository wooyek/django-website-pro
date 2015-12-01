"""
WSGI config for website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

# This will help debug things in the gunicorn environment
print("Importing: %s" % __file__)

import logging
import os
import sys

print("Importing: %s" % __file__)

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)
logging.info('Loading %s', __name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
from .settings import DEV


# determine where is the single absolute path that
# will be used as a reference point for other directories
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
logging.debug("SITE_ROOT: %s" % SITE_ROOT)

# Setup proper logging
from .logcfg import setup_logging
log_file = os.path.join(SITE_ROOT, "logs", 'website.log')
setup_logging(log_file=log_file, console_verbosity=logging.DEBUG if DEV else logging.INFO)

# Obtain WSGIHandler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
