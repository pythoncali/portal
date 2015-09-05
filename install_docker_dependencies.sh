#!/bin/bash

# Add Docker PPA and install latest version
echo 'Adding Docker PPA repository'
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"

echo 'Installing Docker'
apt-get update
apt-get install lxc-docker -y

# Install docker-compose
echo 'Installing Docker Compose'
sh -c "curl -L https://github.com/docker/compose/releases/download/1.4.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose"
chmod +x /usr/local/bin/docker-compose
sh -c "curl -L https://raw.githubusercontent.com/docker/compose/1.4.0/contrib/completion/bash/docker-compose > /etc/bash_completion.d/docker-compose"

# Install docker-cleanup command
echo 'Installing Docker CleaUp command'
cd /tmp
git clone https://gist.github.com/76b450a0c986e576e98b.git
cd 76b450a0c986e576e98b
mv docker-cleanup /usr/local/bin/docker-cleanup
chmod +x /usr/local/bin/docker-cleanup
