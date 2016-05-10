# Gunicorn configuration file
# http://docs.gunicorn.org/en/latest/configure.html#configuration-file

import getpass
import multiprocessing
import socket

HOSTNAME = socket.gethostname().lower()
print("HOSTNAME", HOSTNAME)

if HOSTNAME == "{{ project_name|slugify }}.example.com":
    print("Gunicorn is setting DJANGO_SETTINGS_MODULE in environment")
    raw_env = 'DJANGO_SETTINGS_MODULE=website.settings.production'
elif HOSTNAME != "vagrant":
    print("Gunicorn is setting DJANGO_SETTINGS_MODULE in environment")
    raw_env = 'DJANGO_SETTINGS_MODULE=website.settings.staging'

print("gunicorn user: ", getpass.getuser())
APP_ROOT = "/var/www/{{ project_name }}"

# Setting documentation
# http://docs.gunicorn.org/en/latest/settings.html#settings

proc_name = "{{ project_name }}"
workers = multiprocessing.cpu_count() * 2 + 1
user = "www-data"
group = "www-data"
loglevel = "debug"
bind = "unix:{}/var/gunicorn.sock".format(APP_ROOT)
debug = True
chdir = APP_ROOT + "/src"
accesslog = APP_ROOT + "/logs/gunicorn-access.log"
errorlog = APP_ROOT + "/logs/gunicorn-error.log"

print('workers: ', workers)
