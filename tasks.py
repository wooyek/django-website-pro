# coding=utf-8
# Django Website Pro a template for Django based websites
# Copyright (C) 2015 Janusz Skonieczny
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import sys
from time import sleep
from pathlib import Path
from invoke import run, task

is_win = sys.platform == 'win32'
ROOT_DIR = Path(__file__).parent.absolute()
SRC_DIR = ROOT_DIR / 'src'
VENV_DIR = ROOT_DIR / ".pve"
VENV_BIN = VENV_DIR / ("Scripts" if is_win else "bin")
PYTHON = VENV_BIN / 'python'
PIP = VENV_BIN / 'pip'
MANAGE = '{} {} '.format(PYTHON, SRC_DIR / 'manage.py')


logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)
logging.disable(logging.NOTSET)
logging.debug('Loading %s', __name__)


def virtualenv_activate_this(context_path):
    """By using execfile(this_file, dict(__file__=this_file)) you will
    activate this virtualenv environment.
    This can be used when you must use an existing Python interpreter, not
    the virtualenv bin/python

    A convenience copy of
    https://github.com/pypa/virtualenv/blob/develop/virtualenv_embedded/activate_this.py
    """

    old_os_path = os.environ.get('PATH', '')
    os.environ['PATH'] = os.path.dirname(os.path.abspath(context_path)) + os.pathsep + old_os_path
    base = os.path.dirname(os.path.dirname(os.path.abspath(context_path)))
    if sys.platform == 'win32':
        site_packages = os.path.join(base, 'Lib', 'site-packages')
    else:
        site_packages = os.path.join(base, 'lib', 'python%s' % sys.version[:3], 'site-packages')
    prev_sys_path = list(sys.path)
    import site
    site.addsitedir(site_packages)
    sys.real_prefix = sys.prefix
    sys.prefix = base
    # Move the added items to the front of the path:
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path


def activate_venv():
    # Activate Virtual Environment
    virtualenv_activate_this(str(VENV_BIN))


@task
def bootstrap():
    """
    Setup django project for development
    """
    run('git init', warn=True)
    run('git add *', warn=True)
    run('git commit -m init', warn=True)
    run('git remote add vagrant ssh://vagrant@127.0.0.1:2222/opt/{{project_name}}.git', warn=True)
    create_venv()
    install_requirements()
    run('bower install')
    setup_db()
    run('compass compile styles')


@task
def create_venv():
    """
    Create virtual environment
    """
    logging.debug("Creating venv: %s" % str(VENV_DIR))
    import venv
    venv.main([str(VENV_DIR)])


@task
def install_requirements():
    """
    Install requirements and requirements-dev via pip
    """
    logging.info("Installing requirements")
    # import pip

    if is_win:
        # binary = ROOT_DIR / "arch" / "psycopg2-2.6.1-cp35-none-win_amd64.whl"
        binary = ROOT_DIR / "arch" / "psycopg2-2.6.1-cp35-none-win32.whl"
        cmd = str(PIP) + " install " + str(binary)
        logging.debug("RUN: %s" % cmd)
        run(cmd)

    requirements = ROOT_DIR / "requirements.txt"
    cmd = "{} install -r {} -vvv --upgrade".format(PIP, requirements.absolute())
    logging.debug("RUN: %s" % cmd)
    run(cmd)

    requirements = ROOT_DIR / "requirements-dev.txt"
    cmd = "{} install -r {} -vvv --upgrade".format(PIP, requirements.absolute())
    logging.debug("RUN: %s" % cmd)
    run(cmd)


@task
def setup_db():
    """
    Full database re-initialization
    """

    data = ROOT_DIR / 'data'
    if not data.exists():
        os.makedirs(str(data))

    run(MANAGE + "migrate")
    run(MANAGE + "loaddata "+str(ROOT_DIR / 'fixtures' / 'auth.json'))


@task
def deploy():
    """
    Collect and compile assets, add, commit and push to production remote
    """
    run("compass compile styles")
    run(MANAGE + "assets build")
    run(MANAGE + "collectstatic --noinput")
    run("git add styles static assets templates")
    run("git commit -m deploy")
    run("git push production")

if __name__ == "__main__":
    print("""
To finish setting up a project run:

  inv boostrap


To list all tasks run:

  inv --list


Install invoke first if not yet available

  pip install invoke


I you run on issues OSError, try installing a previous version

  pip install invoke==0.11.1 -U
    """)
