#!/bin/bash

# Setup localizations
echo 'Configuring localizations'
echo 'export LANGUAGE="en_US.UTF-8"' | sudo tee -a /etc/profile.d/lang.sh
echo 'export LANG="en_US.UTF-8"' | sudo tee -a /etc/profile.d/lang.sh
echo 'export LC_ALL="en_US.UTF-8"' | sudo tee -a /etc/profile.d/lang.sh
. /etc/profile.d/lang.sh
locale-gen en_US.UTF-8
sudo dpkg-reconfigure locales

# Install git for version control, pip for install python packages
echo 'Installing pip & virtualenv...'
apt-get update
apt-get install -y python3-pip python-virtualenv python-pip
apt-get install -y postgresql libpq-dev

echo 'Configuring the project virtual enviroment'
mkdir ~vagrant/.virtualenvs
chown vagrant:vagrant ~vagrant/.virtualenvs
virtualenv --python=python3 --no-site-packages ~vagrant/.virtualenvs/env
source ~vagrant/.virtualenvs/env/bin/activate

# Postgres Setup
echo "Configuring Postgres DATABASE"
sudo -u postgres psql postgres -U postgres -c "CREATE ROLE db_user WITH LOGIN ENCRYPTED PASSWORD 'password' CREATEDB CREATEROLE REPLICATION SUPERUSER"
sudo -u postgres psql postgres -U postgres -c "CREATE DATABASE my_db"
sudo -u postgres psql postgres -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE my_db TO db_user"
echo "listen_addresses = '*' " >> /etc/postgresql/9.3/main/postgresql.conf
echo "host    all    all    all    password" >> /etc/postgresql/9.3/main/pg_hba.conf
sudo service postgresql restart

#Install the python requirements (inside the virtualenv)
# Config virtualenv

cd /vagrant/
./install_os_dependencies.sh install
# Commented this because we are already running the deployment process with this
# bash script, but will be available for the moment is needed.
# ./install_docker_dependencies.sh
echo "Installing requirements for python"
pip install -r requirements/local.txt
sudo chown -R vagrant:vagrant ~vagrant/.virtualenvs/

touch config/settings/.env
echo "DATABASE_URL=postgresql://db_user:password@127.0.0.1:5432/my_db" >> config/settings/.env

echo "Setting defaults for when using ssh"
echo "source ~vagrant/.virtualenvs/env/bin/activate" >> ~vagrant/.bashrc
echo "cd /vagrant" >> ~vagrant/.bashrc
python manage.py makemigrations
python manage.py migrate

echo "Project setup finished."
