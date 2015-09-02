#!/usr/bin/env bash

# Use Python 3.4
alias python='/usr/bin/python3.4'
export PYTHONPATH=/usr/lib/python3.4

# Install git for version control, pip for install python packages
echo 'Installing python3-pip...'
apt-get update
apt-get install -y python3-pip

# Install virtualenv
echo 'Installing virtualenv'
alias python='/usr/bin/python3.4'
pip3 install virtualenv
mkdir ~vagrant/.virtualenvs
chown vagrant:vagrant ~vagrant/.virtualenvs
printf "\n\n# Virtualenv settings\n" >> ~vagrant/.bashrc
printf "alias python='/usr/bin/python3.4'\n" >> ~vagrant/.bashrc
virtualenv ~vagrant/.virtualenvs/env
source ~vagrant/.virtualenvs/env/bin/activate

# #Install packages
echo 'export LANGUAGE="en_US.UTF-8"' | sudo tee -a /etc/profile.d/lang.sh
echo 'export LANG="en_US.UTF-8"' | sudo tee -a /etc/profile.d/lang.sh
echo 'export LC_ALL="en_US.UTF-8"' | sudo tee -a /etc/profile.d/lang.sh
. /etc/profile.d/lang.sh

locale-gen en_US.UTF-8
sudo dpkg-reconfigure locales

apt-get -y install python3-dev python3-software-properties
apt-get install -y postgresql-9.3 postgresql-server-dev-9.3
apt-get install -y libjpeg-dev zlib1g-dev
apt-get install -y vim gettext memcached libmemcached-dev


echo "Configure Postgres DATABASE"
sudo -u postgres psql postgres -U postgres -c "CREATE ROLE db_user WITH LOGIN ENCRYPTED PASSWORD 'password' CREATEDB CREATEROLE REPLICATION SUPERUSER"
sudo -u postgres psql postgres -U postgres -c "CREATE DATABASE my_db"
sudo -u postgres psql postgres -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE my_db TO db_user"


echo "listen_addresses = '*' " >> /etc/postgresql/9.3/main/postgresql.conf
echo "host    all    all    all    password" >> /etc/postgresql/9.3/main/pg_hba.conf

sudo service postgresql restart

#Install the python requirements (inside the virtualenv)
cd /vagrant/
echo "Installing requirements for python"
pip3 install -r requirements/local.txt
sudo chown -R vagrant /home/vagrant/.virtualenvs
touch config/settings/.env
echo "DATABASE_URL=postgresql://db_user:password@127.0.0.1:5432/my_db" >> config/settings/.env

echo "Setting defaults for when using ssh"
echo "source ~vagrant/.virtualenvs/env/bin/activate" >> ~vagrant/.bashrc
echo "cd /vagrant" >> ~vagrant/.bashrc
sudo chown -R vagrant:vagrant ~vagrant/.virtualenvs/

python3 manage.py migrate

echo "Project setup finished."
