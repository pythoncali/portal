#!/usr/bin/env bash

#Install packages
echo 'export LANGUAGE="en_US.UTF-8"' | sudo tee -a /etc/profile.d/lang.sh
echo 'export LANG="en_US.UTF-8"' | sudo tee -a /etc/profile.d/lang.sh
echo 'export LC_ALL="en_US.UTF-8"' | sudo tee -a /etc/profile.d/lang.sh
. /etc/profile.d/lang.sh

locale-gen en_US.UTF-8
sudo dpkg-reconfigure locales

apt-get update

apt-get -y install python-dev python-software-properties
apt-get install -y postgresql-9.3 postgresql-server-dev-9.3
apt-get install -y libjpeg-dev zlib1g-dev
apt-get install -y python-virtualenv virtualenvwrapper
apt-get install -y vim gettext memcached libmemcached-dev

#sudo pg_dropcluster --stop 9.3 main
#sudo pg_createcluster --locale en_US.UTF-8 --start 9.3 main

echo "Configure Postgres DATABASE"
sudo -u postgres psql postgres -U postgres -c "CREATE ROLE db_user WITH LOGIN ENCRYPTED PASSWORD 'password' CREATEDB CREATEROLE REPLICATION SUPERUSER"
sudo -u postgres psql postgres -U postgres -c "CREATE DATABASE my_db"
sudo -u postgres psql postgres -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE my_db TO db_user"


echo "listen_addresses = '*' " >> /etc/postgresql/9.3/main/postgresql.conf
echo "host    all    all    all    password" >> /etc/postgresql/9.3/main/pg_hba.conf

sudo service postgresql restart

echo "Configure Virtualenv"
#Create and activate the virtualenv
cd /home/vagrant/
mkdir .virtualenvs
cd .virtualenvs
virtualenv env
source env/bin/activate

#Install the python requirements (inside the virtualenv)
cd /vagrant/
echo "Installing requirments for python"
pip install -r requirements/local.txt
sudo chown -R vagrant /home/vagrant/.virtualenvs
touch config/settings/.env
echo "DATABASE_URL=postgresql://db_user:password@127.0.0.1:5432/my_db" >> config/settings/.env

echo "Setting defaults for when using ssh"
echo "workon env" >> /home/vagrant/.bashrc
echo "cd /vagrant" >> /home/vagrant/.bashrc

echo "Project setup finished."