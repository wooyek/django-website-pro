# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.hostname = "vagrant"
    config.vm.provision "shell", path: "etc/vagrant-setup.sh"
    config.vm.network "private_network", ip: "10.0.0.100"

    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
    end

    # Nginx
    config.vm.network "forwarded_port", host_ip: "127.0.0.1", host: 80, guest: 80

    # Django development server
    config.vm.network "forwarded_port", host_ip: "127.0.0.1", host: 8000, guest: 8000

    # PostgreSQL
    config.vm.network "forwarded_port", host_ip: "127.0.0.1", host: 5432, guest: 5432

    # Supervisor web manager (custom port)
    config.vm.network "forwarded_port", host_ip: "127.0.0.1", host: 9001, guest: 9001

    # RabbitMQ
    # http://www.rabbitmq.com/management.html
    config.vm.network "forwarded_port", host_ip: "127.0.0.1", host: 15672, guest: 15672
    # http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html
    config.vm.network "forwarded_port", host_ip: "127.0.0.1", host: 5672, guest: 5672

end
