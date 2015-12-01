# coding=utf-8
# Created 2014 by Janusz Skonieczny
import logging
import sys
import traceback
from django.core import mail
from django.core.mail import get_connection
from django.views.debug import ExceptionReporter
from pathlib import Path
from django.views.debug import get_exception_reporter_filter


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'short': {
            'format': '%(asctime)s %(levelname)-7s %(thread)-5d %(message)s',
            'datefmt': '%H:%M:%S',
        },
        # this will slow down the app a little, due to
        'verbose': {
            'format': '%(asctime)s %(levelname)-7s %(thread)-5d %(name)s %(filename)s:%(lineno)s | %(funcName)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },

    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'short',
        },
        'mail_admins': {
            'level': 'ERROR',
            # 'class': 'website.logcfg.AdminEmailHandler',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'backupCount': 3,
            'maxBytes': 4194304,  # 4MB
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        # 'django.security.DisallowedHost': {
        #     'handlers': [],
        #     'propagate': False,
        # },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file', 'mail_admins'],
    }
}


def setup_logging(log_file=None, console_verbosity=None, file_verbosity=None):
    if log_file is None:
        log_file = str(Path(__file__).parent.parent.parent / "logs" / "website.log")

    if not Path(log_file).parent.exists():
        Path(log_file).parent.mkdir(parents=True)

    LOGGING['handlers']['file']['level'] = file_verbosity or logging.DEBUG
    LOGGING['handlers']['file']['filename'] = log_file
    LOGGING['handlers']['console']['level'] = console_verbosity or logging.DEBUG

    from logging.config import dictConfig
    dictConfig(LOGGING)
    logging.info("Logging setup changed")
    logging.debug("log_file: %s" % log_file)
    logging.getLogger('spyne.wsgi').setLevel(logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    # Django may do do the configuration somewhere in the future so let's give it our config
    from django.conf import settings
    settings.LOGGING = LOGGING



class AdminEmailHandler(logging.Handler):
    """An exception log handler that emails log entries to site admins.

    If the request is passed as the first argument to the log record,
    request data will be provided in the email report.
    """

    def __init__(self, include_html=False, email_backend=None):
        logging.Handler.__init__(self)
        self.include_html = include_html
        self.email_backend = email_backend

    def emit(self, record):
        try:
            from django.conf import settings
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
                 else 'EXTERNAL'),
                record.getMessage()
            )

            filter = get_exception_reporter_filter(request)
            request_repr = filter.get_request_repr(request)

        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None
            request_repr = "Request repr() unavailable."
        subject = self.format_subject(subject)

        if record.exc_info:
            exc_info = record.exc_info
            stack_trace = '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            exc_info = (None, record.getMessage(), None)
            stack_trace = 'No stack trace available'

        message = '%s: %s' % (record.levelname,record.getMessage())
        message = "%s\n\n%s\n\n%s" % (message, stack_trace, request_repr)
        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        html_message = reporter.get_traceback_html() if self.include_html else None
        mail.mail_admins(subject, message, fail_silently=True,
                         html_message=html_message,
                         connection=self.connection())

    def connection(self):
        return get_connection(backend=self.email_backend, fail_silently=True)

    def format_subject(self, subject):
        """
        Escape CR and LF characters, and limit length.
        RFC 2822's hard limit is 998 characters per line. So, minus "Subject: "
        the actual subject must be no longer than 989 characters.
        """
        formatted_subject = subject.replace('\n', '\\n').replace('\r', '\\r')
        return formatted_subject[:989]
