#!/bin/bash
# ======================================
# System update and common utilities
# ======================================

cat /vagrant/.ssh_key >> .ssh/authorized_keys

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y htop git unzip
sudo apt-get install -y nginx apache2-utils 
sudo apt-get install -y libxml2-dev libxslt1-dev build-essential libpq-dev
sudo apt-get install -y libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
sudo apt-get install -y python python-dev python-pip python-virtualenv supervisor
sudo apt-get install -y python3 python3-dev python3-pip python3.4-venv

# Change Time Zone
# dpkg-reconfigure tzdata
sudo timedatectl set-timezone Europe/Warsaw


# ======================================
# PostgreSQL
# ======================================

sudo apt-get install -y postgresql postgresql-contrib libpq-dev
sudo -u postgres createuser {{project_name}}-user --no-createdb --no-superuser --no-createrole
# Production environment
sudo -u postgres psql -c "ALTER USER {{project_name}}-user WITH PASSWORD '{{ secret_key|slugify|slice:'::2' }}'"
sudo -u postgres createdb direct-billing-db

# For interactive management use
# sudo -i -u postgres


# ======================================
# RabbitMQ
# ======================================

sudo apt-get install -y rabbitmq-server
sudo rabbitmqctl add_user {{project_name}}-user "{{ secret_key|slugify|slice:'1:'|slice:'::3' }}"
sudo rabbitmqctl add_user {{project_name}}-admin "{{ secret_key|slugify|slice:'1:'|slice:'::3' }}"
sudo rabbitmqctl set_user_tags {{project_name}}-admin administrator
sudo rabbitmqctl add_vhost {{project_name}}
sudo rabbitmqctl set_permissions -p {{project_name}} {{project_name}}-user ".*" ".*" ".*"
sudo rabbitmq-plugins enable rabbitmq_management
sudo /etc/init.d/rabbitmq-server restart

# ======================================
# Repo push2deploy
# ======================================

cd /opt/
sudo git init --bare {{project_name}}.git

chmod g+w -R /opt/{{project_name}}.git/
chown :${USER} -R /opt/{{project_name}}.git/
touch /opt/{{project_name}}.git/hooks/post-receive
chmod +x /opt/{{project_name}}.git/hooks/post-receive

cat > /opt/{{project_name}}.git/hooks/post-receive <<EOL
#!/bin/sh
sudo GIT_WORK_TREE=/var/www/{{project_name}} git checkout -f develop
sudo supervisorctl status
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
sudo supervisorctl restart {{project_name}}
sudo supervisorctl restart {{project_name}}-celery
sudo supervisorctl restart {{project_name}}-celery-beat
sudo nginx -s reload
EOL


# ======================================
# Aplikacja WWW
# ======================================

sudo mkdir -p /var/www/{{project_name}}
sudo chown ${USER} -R /var/www/FastRate
cd /var/www/{{project_name}}

mkdir /var/www/{{project_name}}/logs
sudo chown -R :www-data /var/www/{{project_name}}/logs
sudo chmod -R g+rw /var/www/{{project_name}}/logs

mkdir /var/www/{{project_name}}/var
sudo chown -R :www-data /var/www/{{project_name}}/var
sudo chmod -R g+rw /var/www/{{project_name}}/var

mkdir /var/www/{{project_name}}/data
sudo chmod -R g+rw /var/www/{{project_name}}/data
sudo chown -R :www-data /var/www/{{project_name}}/data


# ======================================
# Vagrant development setup
# ======================================


sudo python3 -m venv --clear ~/.pve
# Initial website provisioning until push to deploy takes over
cp /vagrant/requirements.txt /var/www/{{project_name}}/
cp -r /vagrant/etc /var/www/{{project_name}}/
cp -r /vagrant/src /var/www/{{project_name}}/
cp -r /vagrant/templates /var/www/{{project_name}}/
cp -r /vagrant/static /var/www/{{project_name}}/
cp -r /vagrant/vendor /var/www/{{project_name}}/
cp -r /vagrant/assets /var/www/{{project_name}}/
cp -r /vagrant/fixtures /var/www/{{project_name}}/


~/.pve/bin/pip install -r /vagrant/requirements.txt
~/.pve/bin/pip install -r /vagrant/requirements-dev.txt

python3 -m venv --clear /var/www/{{project_name}}/.pve
/var/www/{{project_name}}/.pve/bin/pip install -r /var/www/{{project_name}}/requirements.txt

/var/www/{{project_name}}/.pve/bin/python src/manage.py migrate
/var/www/{{project_name}}/.pve/bin/python src/manage.py loaddata fixtures/auth.json


# ======================================
# Nginx & Supervisor
# ======================================

sudo ln -s /var/www/{{project_name}}/etc/supervisor.conf /etc/supervisor/conf.d/{{project_name}}.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
sudo /etc/init.d/supervisor restart

sudo ln -s /var/www/{{project_name}}/etc/nginx.conf /etc/nginx/sites-available/{{project_name}}.conf
sudo ln -s /etc/nginx/sites-available/{{project_name}}.conf /etc/nginx/sites-enabled/{{project_name}}.conf
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -s reload


