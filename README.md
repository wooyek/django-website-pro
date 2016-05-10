# django-website-pro
Template for Django project, ~~includes~~ will include all the components that usually end up in ~~your~~ my projects.

Usage:

```bash
pip install invoke django
django-admin startproject --extension=py,md,sh,conf --template=https://github.com/wooyek/django-website-pro/archive/master.zip MyProject
cd MyProject
inv bootstrap
```

## What's in the box

1. [x] A more robust folder structure separating code from other project stuff
3. [x] Settings separation for different environment (eg. local vs production)
2. [x] Vagrant setup for quick virtual machine configuration
3. [x] Nginx, gunicorn and supervisor configuration 
4. [x] Git push to deploy repo setup 
5. [ ] Assets management out of the box
6. [ ] Bower configuration for usual front end component
7. [ ] Post startproject setup tasks (venv creation, requirements installation, etc)
8. [ ] Sample SASS and Boostrap based stylesheet and base templates

## Work in progress

This template is already usable as it is, but for now it is based on my previous work and it is heavily opinionated. 
I expect it to change when I'll — with your help — try to make it more universal.
  
Anyway, bacause it's a template there's no need for future support. You should basically take it and modify it to your preferences. 
If have changed it heavily you should consider maintaining a fork, 
private [django project templates](https://docs.djangoproject.com/en/1.9/ref/django-admin/#django-admin-startproject) are a good thing to have.  
