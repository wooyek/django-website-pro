
import socket

HOSTNAME = socket.gethostname()
DEV = HOSTNAME.lower() in ("vagrant", 'odyn')
QA = HOSTNAME.lower().split(".", 1)[0].endswith('qa')

from .local import *
