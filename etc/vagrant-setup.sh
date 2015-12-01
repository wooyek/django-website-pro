#!/bin/bash
# ======================================
# System update and common utilities
# ======================================

cat /vagrant/.ssh_key >> .ssh/authorized_keys

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y htop git unzip
sudo apt-get install -y nginx apache2-utils 
sudo apt-get install -y libxml2-dev libxslt1-dev build-essential
sudo apt-get install -y libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
sudo apt-get install -y python python-dev python-pip python-virtualenv supervisor
sudo apt-get install -y python3 python3-dev python3-pip

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
git init --bare {{project_name}}.git

chmod g+w -R /opt/{{project_name}}.git/
chown :vagrant -R /opt/{{project_name}}.git/
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
sudo nginx -s reload
EOL


# ======================================
# Aplikacja WWW
# ======================================

mkdir -p /var/www/{{project_name}}
cd /var/www/{{project_name}}

mkdir /var/www/{{project_name}}/logs
sudo chown -R :www-data /var/www/{{project_name}}/logs
sudo chmod -R g+rw /var/www/{{project_name}}/logs

mkdir /var/www/{{project_name}}/var
sudo chown -R :www-data /var/www/{{project_name}}/var
sudo chmod -R g+rw /var/www/{{project_name}}/var

mkdir /var/www/{{project_name}}/data
sudo chmod -R g+rw /var/www/{{project_name}}/data
sudo chown :www-data /var/www/{{project_name}}/data


# ======================================
# Vagrant development setup
# ======================================

sudo chown -R vagrant /var/www/{{project_name}}/
sudo chown -R vagrant /opt/{{project_name}}.git/

sudo wget https://bootstrap.pypa.io/get-pip.py
sudo python3 -m venv --without-pip --clear ~/.pve
cp /vagrant/requirements.txt /var/www/{{project_name}}/
cp -r /vagrant/etc /var/www/{{project_name}}/
cp -r /vagrant/src /var/www/{{project_name}}/

sudo ~/.pve/bin/python ./get-pip.py
~/.pve/bin/pip install -r /vagrant/requirements.txt
~/.pve/bin/pip install -r /vagrant/requirements-dev.txt

sudo python3 -m venv --without-pip --clear /var/www/{{project_name}}/.pve
sudo /var/www/{{project_name}}/.pve/bin/python ./get-pip.py
/var/www/{{project_name}}/.pve/bin/pip install -r /var/www/{{project_name}}/requirements.txt

# /var/www/{{project_name}}/.pve/bin/python src/manage.py syncdb
# /var/www/{{project_name}}/.pve/bin/python src/manage.py migrate
# /var/www/{{project_name}}/.pve/bin/python src/manage.py loaddata fixtures/auth.json
rm get-pip.py


# ======================================
# Nginx & Supervisor
# ======================================

ln -s /var/www/{{project_name}}/etc/supervisor.conf /etc/supervisor/conf.d/{{project_name}}.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
sudo /etc/init.d/supervisor restart

ln -s /var/www/{{project_name}}/etc/nginx.conf /etc/nginx/sites-available/{{project_name}}.conf
ln -s /etc/nginx/sites-available/{{project_name}}.conf /etc/nginx/sites-enabled/{{project_name}}.conf
rm /etc/nginx/sites-enabled/default
nginx -s reload


