# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "terrywang/archlinux"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"virtualization

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  # config.vm.provider :virtualbox do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  config.vm.provider :virtualbox do |vb|
    # Uncomment this to enable VirtualBox GUI.
    # vb.gui = true

    # Collect some information about the PWD.
    pwdRealpath = File.realpath('.').to_s
    pwdBasename = File.basename(pwdRealpath)

    # Override default VM image name.
    vb.name = pwdBasename

    # The base box ships with an insufficient home directory size. Begin process
    # of creating new "extension" VM disk and adding to box's LVM.
    # I want disk file to be placed in default machine directory.
    # According to my tests, vb.customize does not return output. In order to
    # determine default machine directory path, I need output of VBoxManage list.
    # This smells. There has to be a better way.
    vBoxSysProperties = Hash.new
    vBoxManageListOutput = `VBoxManage list --long systemproperties`
    vBoxManageListOutput.each_line do |lineString|
      splitLine = lineString.split(':')
      vBoxSysProperties[splitLine[0].strip()] = splitLine[1].strip()
    end

    # The path at which extension disk file will be saved.
    # This file name will not conflict with other machines since each machine
    # is contained in own subdirectory under VBox directory.
    vBoxExtensionDiskPathname = File.join(
      vBoxSysProperties['Default machine folder'],
      vb.name,
      'disk_extension_01.vdi'
    )

    if File.exist?(vBoxExtensionDiskPathname).eql?(false)
      vb.customize [
        'createhd',
        '--filename', vBoxExtensionDiskPathname,
        '--size', 5 * 1024
      ]
    end

    vb.customize [
      'storageattach',
      :id,
      '--storagectl', 'SATA',
      '--port', 1,
      '--device', 0,
      '--type', 'hdd',
      '--medium', vBoxExtensionDiskPathname
    ]

  end

  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL
  config.vm.provision "shell", inline: <<-SHELL
    # Full system upgrade along with specific installs.
    # parted - Used for provisioning extra disk.
    # python-numpy - Used in OpenCV image manipulation.
    # python-pillow - PIL fork. Used for generating NFPA 704 positive samples.
    # xv - Used for Pillow's Image.show()
    sudo pacman -Syu parted python-numpy python-pillow xv --noconfirm
    # Remove orphaned packages.
    sudo pacman -Rns $(pacman -Qtdq) --noconfirm

    # Add extension disk. This is naive in that it uses the /dev/sd? naming which
    # is NOT predictable. UUID should be used but the limited use case of this
    # box means it may not yet be worth it to write code to extract UUIDs.
    sudo parted /dev/sdb mklabel gpt mkpart primary ext4 1MiB 100%
    sudo mkfs.ext4 /dev/sdb1
    sudo -u vagrant mkdir /home/vagrant/abs
    sudo mount /dev/sdb1 /home/vagrant/abs
    sudo chown vagrant:vagrant /home/vagrant/abs
    fstabLine='/dev/sdb1 /home/vagrant/abs ext4 rw,user,data=ordered 0 0'
    sudo printf '\n%s' $fstabLine >> /etc/fstab

    # Enable X forwarding. Enable for a session with 'vagrant ssh -- -X'.
    sudo sed -i 's/#X11Forwarding no/X11Forwarding yes/' /etc/ssh/sshd_config
    sudo systemctl reload sshd

    # Install OpenCV from AUR because opencv is out of date in core (extra).
    # Note that by default, OpenCV build installs proprietary extensions such as
    # IPP. I would disable support for these if I were to use OpenCV more heavily.
    cd /home/vagrant/abs
    sudo -u vagrant git clone https://aur.archlinux.org/opencv-git.git
    cd opencv-git
    sudo -u vagrant makepkg -sr --noconfirm
    sudo pacman -U opencv-git*.pkg.tar.xz --noconfirm

    # Modify alias in vagrant user's .bashrc to personal preference.
    sed -i "s/alias la='ls -A'/alias la='ls -Alh --color'/" /home/vagrant/.bashrc
    source /home/vagrant/.bashrc
  SHELL
end
