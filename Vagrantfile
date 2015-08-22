Vagrant.configure('2') do |config|    

    config.vm.box = 'ubuntu/trusty64'
    config.vm.provision "shell", path: "provision.sh"

    config.ssh.forward_agent = true
    # Forward the dev server port
    config.vm.network :forwarded_port, host: 9000, guest: 8000
    config.vm.network :forwarded_port, host: 5434, guest: 5432
end