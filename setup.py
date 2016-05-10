# coding=utf-8
# Copyright 2014 Janusz Skonieczny
import sys
import os
import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, 'src')
sys.path.append(SRC_DIR)

install_requires = parse_requirements(
    os.path.join(os.path.dirname(__file__), "requirements.txt"),
    session=uuid.uuid1()
)
with open("README.rst") as readme:
    long_description = readme.read()

version = "0.2.2"

setup_kwargs = {
    'name': "{{ project_name|slugify }}",
    'version': version,
    'packages': find_packages("src", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    'package_dir': {'': 'src'},
    'install_requires': [str(r.req) for r in install_requires],

    # "package_data": {
    #     '': ['requirements.txt']
    # },

    'author': "{{ project_name }}",
    'author_email': "{{ project_name|slugify }}@{{ project_name|slugify }}.example.com",
    'description': "{{ project_name }}.description here",
    'long_description': long_description,
    'license': "MIT",
    'keywords': "{{ project_name|slugify }}",
    'url': "https://github.com/{{ project_name|slugify }}/{{ project_name|slugify }}",
    'classifiers': [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    'test_suite': 'website.tests'
}

setup(**setup_kwargs)

